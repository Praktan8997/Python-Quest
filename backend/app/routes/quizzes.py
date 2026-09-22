from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone, timedelta
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.models.models import Quiz, QuizOption, User, QuizAttempt, QuizAnswer, DailyPuzzle
from app.schemas.schemas import QuizSubmitRequest, QuizSubmitResponse, QuizQuestionFeedback, QuizAttemptResponse, DailyPuzzleResponse
from app.services.services import add_user_xp, get_or_create_user_progress, update_topic_mastery

router = APIRouter(tags=["Quizzes"])

def is_answer_correct(q, correct_opt, selected_opt_id, answer_text):
    """Check if answer is correct based on question type."""
    q_type = q.question_type
    if q_type == "fill_in_blank":
        if not answer_text:
            return False
        return answer_text.strip().lower() == correct_opt.option_text.strip().lower()
    elif q_type == "code_output":
        if not answer_text:
            return False
        return answer_text.strip().lower() == correct_opt.option_text.strip().lower()
    else:
        # multiple_choice and true_false
        return (correct_opt is not None) and (correct_opt.id == selected_opt_id)

@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    quiz_id: int,
    req: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct_count = 0
    total_questions = len(quiz.questions)
    feedback_list = []

    user_answers = {ans.question_id: ans for ans in req.answers}

    for q in quiz.questions:
        correct_opt = next((opt for opt in q.options if opt.is_correct), None)
        user_answer = user_answers.get(q.id)
        selected_opt_id = user_answer.selected_option_id if user_answer else 0
        answer_text = user_answer.answer_text if user_answer else None

        is_correct = is_answer_correct(q, correct_opt, selected_opt_id, answer_text)
        if is_correct:
            correct_count += 1

        feedback_list.append(QuizQuestionFeedback(
            question_id=q.id,
            correct_option_id=correct_opt.id if correct_opt else 0,
            selected_option_id=selected_opt_id,
            is_correct=is_correct,
            explanation=q.explanation
        ))

    score = correct_count
    pct = round((correct_count / total_questions * 100.0), 1) if total_questions > 0 else 0.0
    passed = pct >= 70.0

    xp_gained = 0
    new_level = current_user.level

    if passed:
        prog = get_or_create_user_progress(db, current_user.id, quiz.topic_id)
        if not prog.quiz_completed:
            prog.quiz_completed = True
            db.commit()

            new_level, _ = add_user_xp(
                db,
                current_user,
                quiz.xp_reward,
                reason=f"Passed Quiz: {quiz.title}",
                ref_type="quiz",
                ref_id=quiz.id
            )
            xp_gained = quiz.xp_reward

            update_topic_mastery(db, current_user.id, quiz.topic_id)

    # Record QuizAttempt and QuizAnswers in Database
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        total_questions=total_questions,
        percentage=pct,
        passed=passed,
        xp_gained=xp_gained
    )
    db.add(attempt)
    db.flush()

    for fb in feedback_list:
        ans_record = QuizAnswer(
            attempt_id=attempt.id,
            question_id=fb.question_id,
            selected_option_id=fb.selected_option_id,
            is_correct=fb.is_correct
        )
        db.add(ans_record)

    db.commit()

    return QuizSubmitResponse(
        score=score,
        total_questions=total_questions,
        percentage=pct,
        passed=passed,
        xp_gained=xp_gained,
        new_total_xp=current_user.xp,
        new_level=new_level,
        feedback=feedback_list
    )

@router.get("/quizzes/{quiz_id}/attempts", response_model=List[QuizAttemptResponse])
def get_quiz_attempts(quiz_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.quiz_id == quiz_id
    ).order_by(QuizAttempt.created_at.desc()).all()
    return attempts

@router.get("/users/me/quiz-history", response_model=List[QuizAttemptResponse])
def get_user_quiz_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.created_at.desc()).all()
    return attempts

@router.get("/quizzes/daily-puzzle", response_model=DailyPuzzleResponse)
def get_daily_puzzle(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns today's puzzle. Creates one for today if not exists."""
    today = datetime.now(timezone.utc).date()

    puzzle = db.query(DailyPuzzle).filter(
        DailyPuzzle.puzzle_date >= today,
        DailyPuzzle.puzzle_date < today + timedelta(days=1)
    ).first()

    if not puzzle:
        # Select a random quiz question and create a daily puzzle
        quizzes = db.query(Quiz).all()
        if not quizzes:
            raise HTTPException(status_code=404, detail="No quizzes available")

        import random
        quiz = random.choice(quizzes)
        if not quiz.questions:
            raise HTTPException(status_code=404, detail="No questions available")

        question = random.choice(quiz.questions)
        correct_opt = next((opt for opt in question.options if opt.is_correct), None)

        puzzle = DailyPuzzle(
            question_text=question.question_text,
            correct_answer=correct_opt.option_text if correct_opt else "",
            explanation=question.explanation,
            puzzle_date=datetime.now(timezone.utc),
            quiz_id=quiz.id
        )
        db.add(puzzle)
        db.commit()
        db.refresh(puzzle)

    return puzzle

@router.post("/quizzes/daily-puzzle/submit", response_model=QuizSubmitResponse)
def submit_daily_puzzle(
    req: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit today's daily puzzle answer."""
    today = datetime.now(timezone.utc).date()

    puzzle = db.query(DailyPuzzle).filter(
        DailyPuzzle.puzzle_date >= today,
        DailyPuzzle.puzzle_date < today + timedelta(days=1)
    ).first()

    if not puzzle:
        raise HTTPException(status_code=404, detail="No puzzle available for today")

    # Build a mock quiz from the puzzle for reuse of submit logic
    class MockQuiz:
        def __init__(self, puzzle):
            self.id = puzzle.id
            self.title = "Daily Puzzle"
            self.topic_id = puzzle.quiz_id or 1
            self.xp_reward = 50
            self.questions = []

    # Create a mock question with the puzzle data
    mock_question = type('MockQuestion', (), {
        'id': puzzle.id,
        'question_text': puzzle.question_text,
        'explanation': puzzle.explanation,
        'question_type': 'fill_in_blank',
        'options': []
    })()

    if puzzle.correct_answer:
        correct_opt = type('MockOption', (), {
            'id': 1,
            'option_text': puzzle.correct_answer,
            'is_correct': True
        })()
        mock_question.options = [correct_opt]

    mock_quiz = MockQuiz(puzzle)
    mock_quiz.questions = [mock_question]

    # Evaluate answer
    user_answer = req.answers[0] if req.answers else None
    selected_opt_id = user_answer.selected_option_id if user_answer else 0
    answer_text = user_answer.answer_text if user_answer else None

    correct_opt = mock_question.options[0] if mock_question.options else None
    is_correct = is_answer_correct(mock_question, correct_opt, selected_opt_id, answer_text)

    xp_gained = 0
    new_level = current_user.level

    if is_correct:
        prog = get_or_create_user_progress(db, current_user.id, mock_quiz.topic_id)
        if not prog.quiz_completed:
            prog.quiz_completed = True
            db.commit()
            new_level, _ = add_user_xp(
                db, current_user, mock_quiz.xp_reward,
                reason="Daily Puzzle", ref_type="quiz", ref_id=mock_quiz.id
            )
            xp_gained = mock_quiz.xp_reward

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=mock_quiz.id,
        score=1 if is_correct else 0,
        total_questions=1,
        percentage=100.0 if is_correct else 0.0,
        passed=is_correct,
        xp_gained=xp_gained
    )
    db.add(attempt)
    db.flush()

    ans_record = QuizAnswer(
        attempt_id=attempt.id,
        question_id=mock_question.id,
        selected_option_id=selected_opt_id,
        is_correct=is_correct
    )
    db.add(ans_record)
    db.commit()

    return QuizSubmitResponse(
        score=1 if is_correct else 0,
        total_questions=1,
        percentage=100.0 if is_correct else 0.0,
        passed=is_correct,
        xp_gained=xp_gained,
        new_total_xp=current_user.xp,
        new_level=new_level,
        feedback=[QuizQuestionFeedback(
            question_id=mock_question.id,
            correct_option_id=correct_opt.id if correct_opt else 0,
            selected_option_id=selected_opt_id,
            is_correct=is_correct,
            explanation=puzzle.explanation
        )]
    )
