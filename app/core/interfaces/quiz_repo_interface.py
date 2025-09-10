from abc import ABC, abstractmethod


from app.core.schemas.quiz_schemas import QuizInputSchema
from app.infrastructure.postgres.models import Company


class AbstractQuizRepository(ABC):
    @abstractmethod
    async def create(self, company: Company, quiz_payload: QuizInputSchema):
        """Create a new quiz associated with a company."""
        raise NotImplementedError
