from pydantic import BaseModel, Field
from uuid import UUID

class AnswerInputSchema(BaseModel):
    answer_text: str = Field(..., max_length=500)
    is_correct: bool = False

class QuestionInputSchema(BaseModel):
    question_text: str = Field(..., max_length=500)
    answers: list[AnswerInputSchema]

class QuizInputSchema(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    counter: int = Field(default=0)
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

