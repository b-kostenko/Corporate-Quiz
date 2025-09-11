from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.interfaces.quiz_repo_interface import AbstractQuizRepository
from app.core.schemas.quiz_schemas import QuizInputSchema, AnswerInputSchema, QuestionInputSchema
from app.infrastructure.postgres.models import Company, Quiz, Question, Answer

from app.infrastructure.postgres.session_manager import provide_async_session


class QuizRepository(AbstractQuizRepository):

    @provide_async_session
    async def create(self, company: Company, quiz_payload: QuizInputSchema, session: AsyncSession) -> Quiz:
        quiz = await self._create_quiz(company=company, quiz_payload=quiz_payload, session=session)
        for question in quiz_payload.questions:
            created_question = await self._create_questions(quiz_id=quiz.id, question_payload=question, session=session)
            for answer in question.answers:
                await self._create_answers(question_id=created_question.id, answer_payload=answer, session=session)

        await session.commit()

        created_quiz = await self.get(quiz_id=quiz.id, company=company, session=session)
        return created_quiz

    @provide_async_session
    async def get(self, quiz_id: UUID, company: Company, session: AsyncSession) -> Quiz | None:
        stmt = select(Quiz).options(
            selectinload(Quiz.questions).selectinload(Question.answers)
        ).where(Quiz.id == quiz_id, Quiz.company_id == company.id)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @provide_async_session
    async def get_by_id(self, quiz_id: UUID, session: AsyncSession) -> Quiz | None:
        stmt = select(Quiz).options(
            selectinload(Quiz.questions).selectinload(Question.answers)
        ).where(Quiz.id == quiz_id)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @provide_async_session
    async def update(self, quiz: Quiz, quiz_payload: QuizInputSchema, session: AsyncSession) -> Quiz:
        updated_quiz = await self._update_quiz(quiz=quiz, quiz_payload=quiz_payload, session=session)
        # Update questions and answers logic would go here
        for question in quiz_payload.questions:
            updated_question = await self._update_questions(quiz=updated_quiz, question_payload=question, session=session)
            for answer in question.answers:
                await self._update_answers(question=updated_question, answer_payload=answer, session=session)

        await session.commit()
        quiz = await self.get_by_id(quiz_id=quiz.id, session=session)
        return quiz

    @provide_async_session
    async def delete(self, quiz: Quiz, session: AsyncSession) -> None:
        await session.delete(quiz)
        await session.commit()
        return None

    @provide_async_session
    async def get_quizzes_by_company(self, company: Company, limit: int, offset: int, session: AsyncSession) -> tuple[list[Quiz], int]:
        # Get total count
        count_query = select(func.count(Quiz.id))
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        query = (
            select(Quiz)
            .where(Quiz.company_id == company.id)
            .options(selectinload(Quiz.questions).selectinload(Question.answers))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        quizzes = result.scalars().all()

        return list(quizzes), total

    @provide_async_session
    async def _update_quiz(self, quiz: Quiz, quiz_payload: QuizInputSchema, session: AsyncSession) -> Quiz:
        smtp = (
            update(Quiz)
            .where(Quiz.id == quiz.id)
            .values(
                title=quiz_payload.title,
                description=quiz_payload.description,
                counter=quiz_payload.counter,
            )
            .returning(Quiz)
        )
        result = await session.execute(smtp)
        await session.flush()
        return result.scalar_one()

    @provide_async_session
    async def _update_questions(self, quiz: Quiz, question_payload: QuestionInputSchema, session: AsyncSession) -> Question:
        smtp = (
            update(Question)
            .where(Question.quiz_id == quiz.id)
            .values(
                question_text=question_payload.question_text,
            )
            .returning(Question)
        )
        result = await session.execute(smtp)
        await session.flush()
        return result.scalar_one()

    @provide_async_session
    async def _update_answers(self, question: Question, answer_payload: AnswerInputSchema, session: AsyncSession) -> Answer:
        smtp = (
            update(Answer)
            .where(Answer.question_id == question.id)
            .values(
                answer_text=answer_payload.answer_text,
                is_correct=answer_payload.is_correct,
            )
            .returning(Answer)
        )
        result = await session.execute(smtp)
        await session.flush()
        return result.scalar_one()

    @provide_async_session
    async def _create_quiz(self, company: Company, quiz_payload: QuizInputSchema, session: AsyncSession) -> Quiz:
        quiz = Quiz(
            company_id=company.id,
            title=quiz_payload.title,
            description=quiz_payload.description,
        )
        session.add(quiz)
        await session.flush()
        return quiz

    @provide_async_session
    async def _create_questions(self, quiz_id: UUID, question_payload: QuestionInputSchema, session: AsyncSession) -> Question:
        question = Question(
            quiz_id=quiz_id,
            question_text=question_payload.question_text,
        )
        session.add(question)
        await session.flush()
        return question

    @provide_async_session
    async def _create_answers(self, question_id: UUID, answer_payload: AnswerInputSchema, session: AsyncSession) -> Answer:
        answer = Answer(
            question_id=question_id,
            answer_text=answer_payload.answer_text,
            is_correct=answer_payload.is_correct,
        )
        session.add(answer)
        await session.flush()
        return answer