import json
from uuid import UUID

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.interfaces.quiz_repo_interface import AbstractQuizRepository
from app.core.repositories.redis_repository import AsyncRedisRepository
from app.core.schemas import PaginatedResponse, PaginationMeta
from app.core.schemas.quiz_schemas import (
    AnswerUserResultSchema,
    AttemptQuizInputSchema,
    AttemptQuizResultSchema,
    QuestionUserResultSchema,
    QuizAttemptRedisSchema,
    QuizInputSchema,
    QuizOutputSchema,
)
from app.infrastructure.postgres.models import Quiz, User
from app.infrastructure.postgres.models.enums import CompanyMemberRole
from app.utils.exceptions import ObjectNotFound, PermissionDenied


class QuizService:
    def __init__(self, company_repository, quiz_repository, redis_repository):
        self.company_repository: AbstractCompanyRepository = company_repository
        self.quiz_repository: AbstractQuizRepository = quiz_repository
        self.redis_repository: AsyncRedisRepository = redis_repository

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
            total=total, limit=limit, offset=offset, has_next=offset + limit < total, has_previous=offset > 0
        )
        return PaginatedResponse[QuizOutputSchema](items=quiz_schemas, meta=meta)

    async def calculate_score(self, quiz_payload: AttemptQuizInputSchema, quiz: Quiz) -> AttemptQuizResultSchema:
        correct_count = 0
        total_questions = len(quiz.questions)
        answers_detail = []

        for quiz_question, user_question in zip(quiz.questions, quiz_payload.questions):
            if quiz_question.question_text != user_question.question_text:
                continue

            correct_answers = {ans.answer_text for ans in quiz_question.answers if ans.is_correct}
            user_correct_answers = {ans.answer_text for ans in user_question.answers if ans.is_correct}

            is_question_correct = correct_answers == user_correct_answers
            if is_question_correct:
                correct_count += 1

            answers_for_question = [
                AnswerUserResultSchema(
                    answer_text=ans.answer_text,
                    is_correct=ans.answer_text in correct_answers
                ) for ans in user_question.answers
            ]

            answers_detail.append(
                QuestionUserResultSchema(
                    question_text=quiz_question.question_text,
                    answers=answers_for_question
                )
            )

        score_percent = round((correct_count / total_questions) * 100, 2)
        return AttemptQuizResultSchema(
            score=score_percent,
            total_questions=total_questions,
            correct_answers_count=correct_count,
            answers_detail=answers_detail
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

        quiz_attempt_key = f"quiz_attempt:{user.id}:{company.id}:{quiz.id}"
        quiz_attempt_value = QuizAttemptRedisSchema(
            user_id=user.id,
            company_id=company.id,
            quiz_id=quiz.id,
            score=result.score,
            total_questions=result.total_questions,
            correct_answers_count=result.correct_answers_count,
            answers_detail=result.answers_detail,
        ).model_dump_json()

        await self.redis_repository.set(
            key=quiz_attempt_key,
            value=quiz_attempt_value,
            ex=48 * 60 * 60,  # 48 hours expiration
        )

        attempt = await self.quiz_repository.record_quiz_attempt(user=user, quiz=quiz, company=company, score=result)
        return attempt

    async def get_quiz_attempts(self, quiz_id: UUID, company_id: UUID, user: User):
        company = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        company_member = await self.company_repository.get_company_member(company=company, user_id=user.id)
        if not company_member:
            raise PermissionDenied("You are not a member of this company.")

        quiz = await self.quiz_repository.get(quiz_id=quiz_id, company=company)
        if not quiz:
            raise ObjectNotFound(model_name="Quiz", id_=quiz_id)

        quiz_attempt_key = f"quiz_attempt:{user.id}:{company.id}:{quiz.id}"
        attempt = await self.redis_repository.get(key=quiz_attempt_key)
        if not attempt:
            return []

        quiz_schema = QuizAttemptRedisSchema.model_validate(json.loads(attempt))
        return quiz_schema