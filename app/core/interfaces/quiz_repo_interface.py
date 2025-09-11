from abc import ABC, abstractmethod
from uuid import UUID

from app.core.schemas.quiz_schemas import QuizInputSchema
from app.infrastructure.postgres.models import Company, Quiz


class AbstractQuizRepository(ABC):
    @abstractmethod
    async def create(self, company: Company, quiz_payload: QuizInputSchema):
        """Create a new quiz associated with a company."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, quiz_id: UUID, company: Company):
        """Retrieve a quiz by its ID and associated company."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, quiz: Quiz, quiz_payload: QuizInputSchema):
        """Update an existing quiz with new data."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, quiz: Quiz):
        """Delete a quiz from the database."""
        raise NotImplementedError

    @abstractmethod
    async def get_quizzes_by_company(self, company: Company, limit: int, offset: int):
        """Retrieve quizzes associated with a specific company, with pagination."""
        raise NotImplementedError