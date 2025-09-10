from pydantic import UUID4

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.interfaces.quiz_repo_interface import AbstractQuizRepository
from app.core.schemas.quiz_schemas import QuizInputSchema
from app.infrastructure.postgres.models import User
from app.utils.exceptions import ObjectNotFound


class QuizService:

    def __init__(self, company_repository: AbstractCompanyRepository, quiz_repository: AbstractQuizRepository):
        self.company_repository: AbstractCompanyRepository = company_repository
        self.quiz_repository: AbstractQuizRepository = quiz_repository

    async def create(self, company_id: UUID4, user: User, quiz_payload: QuizInputSchema):
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        quiz = await self.quiz_repository.create(company=company, quiz_payload=quiz_payload)

        return quiz