from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.models.models import Challenge, User, Submission
from app.schemas.schemas import CodeSubmitRequest, CodeSubmitResponse, SubmissionResponse
from app.services.services import execute_code_remote, add_user_xp, get_or_create_user_progress, update_topic_mastery

router = APIRouter(tags=["Challenges"])

@router.get("/challenges/{challenge_id}", response_model=dict)
def get_challenge_by_id(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return {
        "id": challenge.id,
        "topic_id": challenge.topic_id,
        "title": challenge.title,
        "description": challenge.description,
        "difficulty": challenge.difficulty,
        "starter_code": challenge.starter_code,
        "xp_reward": challenge.xp_reward,
        "hint": challenge.hint,
        "solution_explanation": challenge.solution_explanation,
        "test_cases": [
            {"id": tc.id, "input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden}
            for tc in challenge.test_cases if not tc.is_hidden
        ]
    }

@router.post("/challenges/{challenge_id}/run", response_model=CodeSubmitResponse)
async def run_challenge_dry(
    challenge_id: int,
    req: CodeSubmitRequest,
    db: Session = Depends(get_db)
):
    """Dry run code execution against test cases without saving submission or awarding XP."""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    tc_list = [
        {"input": tc.input_data or "", "expected_output": tc.expected_output}
        for tc in challenge.test_cases
    ]

    exec_result = await execute_code_remote(req.code, tc_list)
    success = exec_result.get("success", False)
    all_passed = exec_result.get("all_tests_passed", False) or success

    return CodeSubmitResponse(
        success=success,
        passed=all_passed,
        stdout=exec_result.get("stdout", ""),
        stderr=exec_result.get("stderr", ""),
        error=exec_result.get("error"),
        xp_gained=0,
        new_total_xp=0,
        new_level=1,
        leveled_up=False,
        test_results=exec_result.get("test_results", [])
    )

@router.post("/challenges/{challenge_id}/submit", response_model=CodeSubmitResponse)
async def submit_challenge(
    challenge_id: int,
    req: CodeSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Formal code submission running test cases, creating Submission record, and awarding XP."""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    tc_list = [
        {"input": tc.input_data or "", "expected_output": tc.expected_output}
        for tc in challenge.test_cases
    ]

    exec_result = await execute_code_remote(req.code, tc_list)
    success = exec_result.get("success", False)
    all_passed = exec_result.get("all_tests_passed", False) or success
    stdout = exec_result.get("stdout", "")
    stderr = exec_result.get("stderr", "")

    # Save Submission entity to database
    sub = Submission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        code=req.code,
        success=success,
        passed=all_passed,
        stdout=stdout,
        stderr=stderr,
        execution_time_ms=exec_result.get("execution_time_ms", 0.0)
    )
    db.add(sub)
    db.commit()

    xp_gained = 0
    new_level = current_user.level
    leveled_up = False

    if all_passed:
        prog = get_or_create_user_progress(db, current_user.id, challenge.topic_id)
        if not prog.challenge_completed:
            prog.challenge_completed = True
            db.commit()

            new_level, leveled_up = add_user_xp(
                db,
                current_user,
                challenge.xp_reward,
                reason=f"Completed Challenge: {challenge.title}",
                ref_type="challenge",
                ref_id=challenge.id
            )
            xp_gained = challenge.xp_reward

            update_topic_mastery(db, current_user.id, challenge.topic_id)

    return CodeSubmitResponse(
        success=success,
        passed=all_passed,
        stdout=stdout,
        stderr=stderr,
        error=exec_result.get("error"),
        xp_gained=xp_gained,
        new_total_xp=current_user.xp,
        new_level=new_level,
        leveled_up=leveled_up,
        test_results=exec_result.get("test_results", [])
    )

@router.get("/users/me/submissions", response_model=List[SubmissionResponse])
def get_user_submissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subs = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).order_by(Submission.created_at.desc()).all()
    return subs
