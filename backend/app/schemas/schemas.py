from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Auth & User Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    level: int
    xp: int
    current_streak: int
    longest_streak: int = 1
    created_at: datetime

# Topic & Curriculum Schemas
class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    content: str
    code_example: Optional[str] = None
    order_index: int

class ChallengeTestCaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    input_data: Optional[str] = ""
    expected_output: str
    is_hidden: bool

class ChallengeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    description: str
    difficulty: str
    starter_code: str
    xp_reward: int
    hint: Optional[str] = None
    solution_explanation: Optional[str] = None
    test_cases: List[ChallengeTestCaseResponse] = []

class QuizOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    option_text: str

class QuizQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    question_text: str
    question_type: str = "multiple_choice"
    options: List[QuizOptionResponse] = []

class QuizResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    description: Optional[str] = None
    xp_reward: int
    questions: List[QuizQuestionResponse] = []

# Submissions & Attempts Schemas
class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    challenge_id: int
    code: str
    success: bool
    passed: bool
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    execution_time_ms: float
    created_at: datetime

class QuizAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: float
    passed: bool
    xp_gained: int
    created_at: datetime

# Progress & Challenge Submission
class CodeSubmitRequest(BaseModel):
    code: str

class TestCaseResultResponse(BaseModel):
    input: str
    expected_output: str
    actual_output: str
    passed: bool

class CodeSubmitResponse(BaseModel):
    success: bool
    passed: bool
    stdout: str
    stderr: str
    error: Optional[str] = None
    xp_gained: int = 0
    new_total_xp: int = 0
    new_level: int = 1
    leveled_up: bool = False
    test_results: List[TestCaseResultResponse] = []

class QuizSubmitAnswer(BaseModel):
    question_id: int
    selected_option_id: int = 0
    answer_text: Optional[str] = None

class QuizSubmitRequest(BaseModel):
    answers: List[QuizSubmitAnswer]

class DailyPuzzleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    explanation: Optional[str] = None
    puzzle_date: datetime
    quiz_id: Optional[int] = None

class QuizQuestionFeedback(BaseModel):
    question_id: int
    correct_option_id: int
    selected_option_id: int
    is_correct: bool
    explanation: Optional[str] = None

class QuizSubmitResponse(BaseModel):
    score: int
    total_questions: int
    percentage: float
    passed: bool
    xp_gained: int
    new_total_xp: int
    new_level: int
    feedback: List[QuizQuestionFeedback]

class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    level_number: int
    level_title: str
    order_index: int
    description: str
    icon: str
    is_completed: Optional[bool] = False
    lessons_count: Optional[int] = 0
    challenges_count: Optional[int] = 0

class LeaderboardEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rank: int
    user_id: int
    username: str
    full_name: Optional[str] = None
    xp: int
    level: int
    streak: int

class BadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    icon: str
    earned: bool = False
    earned_at: Optional[datetime] = None

class UserProgressSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    xp: int
    level: int
    next_level_xp: int
    xp_in_level: int
    xp_to_next_level: int
    xp_level_percentage: float
    current_streak: int
    longest_streak: int
    topics_mastered: int
    total_topics: int
    progress_percentage: float
    recent_activity: List[dict] = []
    recent_submissions: List[SubmissionResponse] = []
    recent_quiz_attempts: List[QuizAttemptResponse] = []
