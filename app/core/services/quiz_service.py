from uuid import UUID

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.interfaces.quiz_repo_interface import AbstractQuizRepository
from app.core.schemas import PaginationMeta, PaginatedResponse
from app.core.schemas.quiz_schemas import QuizInputSchema, QuizOutputSchema
from app.infrastructure.postgres.models import User
from app.infrastructure.postgres.models.enums import CompanyMemberRole
from app.utils.exceptions import ObjectNotFound, PermissionDenied


class QuizService:

    def __init__(self, company_repository: AbstractCompanyRepository, quiz_repository: AbstractQuizRepository):
        self.company_repository: AbstractCompanyRepository = company_repository
        self.quiz_repository: AbstractQuizRepository = quiz_repository

    async def create(self, company_id: UUID, user: User, quiz_payload: QuizInputSchema):
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if company_member.role not in [CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN]:
            raise PermissionDenied("Only company owners and admins can create quizzes.")

        quiz = await self.quiz_repository.create(company=company, quiz_payload=quiz_payload)

        return quiz

    async def update(self, quiz_id: UUID, company_id: UUID, user: User, quiz_payload: QuizInputSchema):
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if company_member.role not in [CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN]:
            raise PermissionDenied("Only company owners and admins can update quizzes.")

        quiz = await self.quiz_repository.get(quiz_id=quiz_id, company=company)
        if not quiz:
            raise ObjectNotFound(model_name="Quiz", id_=quiz_id)

        updated_quiz = await self.quiz_repository.update(quiz=quiz, quiz_payload=quiz_payload)

        return updated_quiz

    async def delete(self, quiz_id: UUID, company_id: UUID, user: User):
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if company_member.role not in [CompanyMemberRole.OWNER]:
            raise PermissionDenied("Only company owners can delete quizzes.")

        quiz = await self.quiz_repository.get(quiz_id=quiz_id, company=company)
        if not quiz:
            raise ObjectNotFound(model_name="Quiz", id_=quiz_id)

        await self.quiz_repository.delete(quiz=quiz)

    async def get_company_quizzes(self, company_id: UUID, user: User, limit: int = 10, offset: int = 0):
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if not company_member:
            raise PermissionDenied("You are not a member of this company.")

        quizzes, total = await self.quiz_repository.get_quizzes_by_company(company=company, limit=limit, offset=offset)
        quiz_schemas = [QuizOutputSchema.model_validate(quiz) for quiz in quizzes]

        meta = PaginationMeta(
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
            has_previous=offset > 0
        )
        return PaginatedResponse[QuizOutputSchema](items=quiz_schemas, meta=meta)