from uuid import UUID

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.interfaces.quiz_repo_interface import AbstractQuizRepository
from app.core.schemas import PaginationMeta, PaginatedResponse
from app.core.schemas.quiz_schemas import QuizInputSchema, QuizOutputSchema, AttemptQuizInputSchema, QuizResultSchema
from app.infrastructure.postgres.models import User, Quiz
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

    async def calculate_score(self, quiz_payload: AttemptQuizInputSchema, quiz: Quiz):
        correct_count = 0
        total_questions = len(quiz.questions)

        for quiz_question, user_question in zip(quiz.questions, quiz_payload.questions):
            if quiz_question.question_text != user_question.question_text:
                continue

            correct_answers = {ans.answer_text for ans in quiz_question.answers if ans.is_correct}

            user_correct_answers = {ans.answer_text for ans in user_question.answers if ans.is_correct}

            if correct_answers == user_correct_answers:
                correct_count += 1

        score_percent = round((correct_count / total_questions) * 100, 2)
        return QuizResultSchema(
            score=score_percent,
            total_questions=total_questions,
            correct_answers_count=correct_count
        )

    async def attempt_quiz(self, quiz_payload: AttemptQuizInputSchema, quiz_id: UUID, company_id: UUID, user: User):
        company = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if not company_member:
            raise PermissionDenied("You are not a member of this company.")

        quiz = await self.quiz_repository.get(quiz_id=quiz_id, company=company)
        if not quiz:
            raise ObjectNotFound(model_name="Quiz", id_=quiz_id)

        result = await self.calculate_score(quiz_payload=quiz_payload, quiz=quiz)

        attempt = await self.quiz_repository.record_quiz_attempt(user=user, quiz=quiz, company=company, score=result)
        return attempt

