from pydantic import BaseModel, Field, UUID4


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
    id: UUID4
    question_id: UUID4
    answer_text: str
    is_correct: bool

    class Config:
        from_attributes = True

class QuestionOutputSchema(BaseModel):
    id: UUID4
    quiz_id: UUID4
    question_text: str
    answers: list[AnswerOutputSchema] = []

    class Config:
        from_attributes = True

class QuizOutputSchema(BaseModel):
    id: UUID4
    company_id: UUID4
    title: str
    description: str
    counter: int
    questions: list[QuestionOutputSchema] = []

    class Config:
        from_attributes = True

