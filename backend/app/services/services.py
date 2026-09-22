import math
import httpx
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.models import User, XPTransaction, UserProgress, UserBadge, Badge, Topic
from app.core.config import settings

# Milestone XP Thresholds specified in gemini.md
LEVEL_THRESHOLDS = [0, 100, 250, 500, 850, 1300, 1900, 2600, 3500, 4500, 6000, 8000, 10500, 13500, 17000]

def calculate_level(xp: int) -> int:
    """Calculates level index based on milestone XP curve."""
    if xp <= 0:
        return 1
    for idx, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp < threshold:
            return idx
    return len(LEVEL_THRESHOLDS)

def get_level_info(xp: int) -> dict:
    """Calculates level, next level XP target, and percentage progress toward next level."""
    lvl = calculate_level(xp)
    prev_threshold = LEVEL_THRESHOLDS[lvl - 1] if lvl - 1 < len(LEVEL_THRESHOLDS) else LEVEL_THRESHOLDS[-1]
    
    if lvl < len(LEVEL_THRESHOLDS):
        next_threshold = LEVEL_THRESHOLDS[lvl]
    else:
        next_threshold = prev_threshold + 5000

    xp_in_level = max(0, xp - prev_threshold)
    xp_needed_for_level = max(1, next_threshold - prev_threshold)
    xp_to_next_level = max(0, next_threshold - xp)
    xp_level_pct = round(min(100.0, max(0.0, (xp_in_level / xp_needed_for_level) * 100.0)), 1)

    return {
        "level": lvl,
        "current_xp": xp,
        "prev_level_xp": prev_threshold,
        "next_level_xp": next_threshold,
        "xp_in_level": xp_in_level,
        "xp_to_next_level": xp_to_next_level,
        "xp_level_percentage": xp_level_pct
    }

def update_user_activity_streak(user: User):
    """Updates current_streak and longest_streak based on meaningful activity timestamps."""
    now = datetime.now(timezone.utc)
    if not user.longest_streak:
        user.longest_streak = 1
    
    if user.last_activity_date:
        diff_days = (now.date() - user.last_activity_date.date()).days
        if diff_days == 1:
            user.current_streak += 1
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
        elif diff_days > 1:
            user.current_streak = 1
    else:
        user.current_streak = 1
        user.longest_streak = 1
    
    user.last_activity_date = now

def add_user_xp(db: Session, user: User, amount: int, reason: str, ref_type: str = None, ref_id: int = None) -> tuple[int, bool]:
    """Awards XP to user, records transaction, updates level/streak, and returns (new_level, leveled_up)."""
    old_level = user.level
    user.xp += amount
    
    lvl_info = get_level_info(user.xp)
    new_level = lvl_info["level"]
    leveled_up = new_level > old_level
    user.level = new_level

    # Update streak & activity
    update_user_activity_streak(user)

    # Record XP transaction
    tx = XPTransaction(
        user_id=user.id,
        amount=amount,
        reason=reason,
        reference_type=ref_type,
        reference_id=ref_id
    )
    db.add(tx)
    db.commit()
    db.refresh(user)

    # Check and award badges
    check_and_award_badges(db, user)

    return new_level, leveled_up

def get_or_create_user_progress(db: Session, user_id: int, topic_id: int) -> UserProgress:
    prog = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    if not prog:
        prog = UserProgress(user_id=user_id, topic_id=topic_id)
        db.add(prog)
        db.commit()
        db.refresh(prog)
    return prog

def update_topic_mastery(db: Session, user_id: int, topic_id: int):
    prog = get_or_create_user_progress(db, user_id, topic_id)
    if prog.challenge_completed and prog.quiz_completed:
        prog.is_mastered = True
        db.commit()

def check_and_award_badges(db: Session, user: User):
    badges = db.query(Badge).all()
    earned_badge_ids = {ub.badge_id for ub in user.user_badges}

    mastered_count = db.query(UserProgress).filter(
        UserProgress.user_id == user.id,
        UserProgress.is_mastered == True
    ).count()

    for badge in badges:
        if badge.id in earned_badge_ids:
            continue
        
        should_award = False
        if badge.criteria_type == "first_program" and user.xp > 0:
            should_award = True
        elif badge.criteria_type == "streak" and (user.current_streak >= int(badge.criteria_value) or user.longest_streak >= int(badge.criteria_value)):
            should_award = True
        elif badge.criteria_type == "topics_mastered" and mastered_count >= int(badge.criteria_value):
            should_award = True
        elif badge.criteria_type == "level" and user.level >= int(badge.criteria_value):
            should_award = True

        if should_award:
            ub = UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(ub)
    db.commit()

async def execute_code_remote(code: str, test_cases: list) -> dict:
    """Sends code to execution service endpoint."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        payload = {
            "code": code,
            "timeout": 3.0,
            "test_cases": test_cases
        }
        try:
            resp = await client.post(settings.CODE_EXECUTION_URL, json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Execution service returned HTTP {resp.status_code}",
                    "error": "Execution Service Error"
                }
        except Exception as e:
            return fallback_local_execution(code, test_cases)

def fallback_local_execution(code: str, test_cases: list) -> dict:
    import sys
    import subprocess
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        if not test_cases:
            proc = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=3.0)
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "error": proc.stderr.strip() if proc.returncode != 0 else None,
                "all_tests_passed": proc.returncode == 0
            }
        
        test_results = []
        all_passed = True
        overall_stdout = ""
        overall_stderr = ""

        for tc in test_cases:
            tc_input = tc.get("input", "") or ""
            expected = tc.get("expected_output", "").strip()
            proc = subprocess.run([sys.executable, tmp_path], input=tc_input, capture_output=True, text=True, timeout=3.0)
            actual = proc.stdout.strip()
            passed = (proc.returncode == 0) and (actual == expected)
            if not passed:
                all_passed = False
            test_results.append({
                "input": tc_input,
                "expected_output": expected,
                "actual_output": actual if proc.returncode == 0 else proc.stderr.strip(),
                "passed": passed
            })
            if actual:
                overall_stdout += actual + "\n"
            if proc.stderr:
                overall_stderr += proc.stderr + "\n"

        return {
            "success": all_passed,
            "stdout": overall_stdout.strip(),
            "stderr": overall_stderr.strip(),
            "all_tests_passed": all_passed,
            "test_results": test_results
        }
    except Exception as ex:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(ex),
            "error": "Local execution error"
        }
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
