from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.models.models import User, UserProgress, Topic, Badge, XPTransaction, Submission, QuizAttempt
from app.schemas.schemas import LeaderboardEntry, UserProgressSummary, BadgeResponse, SubmissionResponse, QuizAttemptResponse
from app.services.services import get_level_info

router = APIRouter(tags=["Leaderboard & Progress"])

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(limit: int = 50, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).limit(limit).all()
    res = []
    for idx, u in enumerate(users, start=1):
        res.append(LeaderboardEntry(
            rank=idx,
            user_id=u.id,
            username=u.username,
            full_name=u.full_name,
            xp=u.xp,
            level=u.level,
            streak=u.current_streak
        ))
    return res

@router.get("/progress", response_model=UserProgressSummary)
def get_user_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_topics = db.query(Topic).count()
    mastered_count = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.is_mastered == True
    ).count()

    pct = round((mastered_count / total_topics * 100.0), 1) if total_topics > 0 else 0.0

    lvl_info = get_level_info(current_user.xp)

    recent_txs = db.query(XPTransaction).filter(
        XPTransaction.user_id == current_user.id
    ).order_by(XPTransaction.created_at.desc()).limit(5).all()

    activity = [
        {
            "id": tx.id,
            "amount": tx.amount,
            "reason": tx.reason,
            "date": tx.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for tx in recent_txs
    ]

    recent_subs = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).order_by(Submission.created_at.desc()).limit(5).all()

    recent_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.created_at.desc()).limit(5).all()

    return UserProgressSummary(
        xp=current_user.xp,
        level=current_user.level,
        next_level_xp=lvl_info["next_level_xp"],
        xp_in_level=lvl_info["xp_in_level"],
        xp_to_next_level=lvl_info["xp_to_next_level"],
        xp_level_percentage=lvl_info["xp_level_percentage"],
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak or current_user.current_streak,
        topics_mastered=mastered_count,
        total_topics=total_topics,
        progress_percentage=pct,
        recent_activity=activity,
        recent_submissions=recent_subs,
        recent_quiz_attempts=recent_attempts
    )

@router.get("/badges", response_model=List[BadgeResponse])
def get_badges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    badges = db.query(Badge).all()
    user_badge_map = {ub.badge_id: ub.earned_at for ub in current_user.user_badges}

    res = []
    for b in badges:
        earned = b.id in user_badge_map
        res.append(BadgeResponse(
            id=b.id,
            name=b.name,
            description=b.description,
            icon=b.icon,
            earned=earned,
            earned_at=user_badge_map.get(b.id)
        ))
    return res
