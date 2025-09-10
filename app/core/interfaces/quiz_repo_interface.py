from abc import ABC, abstractmethod

from pydantic import UUID4

from app.core.schemas.quiz_schemas import QuizInputSchema, QuestionInputSchema, AnswerInputSchema
from app.infrastructure.postgres.models import Company, Quiz, Question, Answer


class AbstractQuizRepository(ABC):
    @abstractmethod
    async def create(self, company: Company, quiz_payload: QuizInputSchema):
        """Create a new quiz associated with a company."""
        raise NotImplementedError

    @abstractmethod
    async def _create_quiz(self, company: Company, quiz_payload: QuizInputSchema) -> Quiz:
        """Create a new quiz associated with a company."""
        raise NotImplementedError

    @abstractmethod
    async def _create_questions(self, quiz_id: UUID4, question_payload: QuestionInputSchema) -> Question:
        """Create a new question associated with a quiz."""
        raise NotImplementedError

    @abstractmethod
    async def _create_answers(self, question_id: UUID4, answer_payload: AnswerInputSchema) -> Answer:
        """Create a new answer associated with a question."""
        raise NotImplementedError