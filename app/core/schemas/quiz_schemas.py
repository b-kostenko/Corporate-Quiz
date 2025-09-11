from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AnswerInputSchema(BaseModel):
    answer_text: str = Field(..., max_length=500)
    is_correct: bool = False


class QuestionInputSchema(BaseModel):
    question_text: str = Field(..., max_length=500)
    answers: list[AnswerInputSchema]


class QuizInputSchema(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    questions: list[QuestionInputSchema]


class AnswerOutputSchema(BaseModel):
    id: UUID
    question_id: UUID
    answer_text: str
    is_correct: bool

    class Config:
        from_attributes = True


class QuestionOutputSchema(BaseModel):
    id: UUID
    quiz_id: UUID
    question_text: str
    answers: list[AnswerOutputSchema] = []

    class Config:
        from_attributes = True


class QuizOutputSchema(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    description: str
    counter: int
    questions: list[QuestionOutputSchema] = []

    class Config:
        from_attributes = True


class QuizResultSchema(BaseModel):
    score: float
    total_questions: int
    correct_answers_count: int


class AttemptQuizInputSchema(BaseModel):
    questions: list[QuestionInputSchema]


class AttemptQuizOutputSchema(QuizResultSchema):
    quiz_id: UUID
    user_id: UUID
    company_id: UUID
    last_attempt_time: datetime

    class Config:
        from_attributes = True
