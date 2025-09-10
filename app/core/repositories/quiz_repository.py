from uuid import UUID

from sqlalchemy import select
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

        stmt = select(Quiz).options(
            selectinload(Quiz.questions).selectinload(Question.answers)
        ).where(Quiz.id == quiz.id)
        
        result = await session.execute(stmt)
        quiz_with_relations = result.scalar_one()
        
        return quiz_with_relations

    @provide_async_session
    async def _create_quiz(self, company: Company, quiz_payload: QuizInputSchema, session: AsyncSession) -> Quiz:
        quiz = Quiz(
            company_id=company.id,
            title=quiz_payload.title,
            description=quiz_payload.description,
            counter=quiz_payload.counter,
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