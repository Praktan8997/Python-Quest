from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.routes.auth import get_current_user_optional
from app.models.models import Topic, Lesson, Challenge, Quiz, UserProgress, User
from app.schemas.schemas import TopicResponse, LessonResponse, ChallengeResponse, QuizResponse

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_optional)):
    topics = db.query(Topic).order_by(Topic.order_index).all()
    
    user_prog = {}
    if current_user:
        progs = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
        user_prog = {p.topic_id: p.is_mastered for p in progs}

    res = []
    for t in topics:
        res.append(TopicResponse(
            id=t.id,
            title=t.title,
            slug=t.slug,
            level_number=t.level_number,
            level_title=t.level_title,
            order_index=t.order_index,
            description=t.description,
            icon=t.icon,
            is_completed=user_prog.get(t.id, False),
            lessons_count=len(t.lessons),
            challenges_count=len(t.challenges)
        ))
    return res

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_by_id(topic_id: int, db: Session = Depends(get_db)):
    t = db.query(Topic).filter(Topic.id == topic_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Topic not found")
    return TopicResponse(
        id=t.id,
        title=t.title,
        slug=t.slug,
        level_number=t.level_number,
        level_title=t.level_title,
        order_index=t.order_index,
        description=t.description,
        icon=t.icon,
        is_completed=False,
        lessons_count=len(t.lessons),
        challenges_count=len(t.challenges)
    )

@router.get("/{topic_id}/lessons", response_model=List[LessonResponse])
def get_topic_lessons(topic_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.topic_id == topic_id).order_by(Lesson.order_index).all()
    return lessons

@router.get("/{topic_id}/challenges", response_model=List[ChallengeResponse])
def get_topic_challenges(topic_id: int, db: Session = Depends(get_db)):
    challenges = db.query(Challenge).filter(Challenge.topic_id == topic_id).all()
    return challenges

@router.get("/{topic_id}/quizzes", response_model=List[QuizResponse])
def get_topic_quizzes(topic_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.topic_id == topic_id).all()
    return quizzes
