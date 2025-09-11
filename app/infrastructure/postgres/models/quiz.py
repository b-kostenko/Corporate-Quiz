from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.postgres.models.base import BaseModelMixin


class Quiz(BaseModelMixin):
    __tablename__ = "quizzes"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    counter: Mapped[int] = mapped_column(default=0)

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    user_attempts = relationship(
        "UserQuizAttempt", back_populates="quiz"
    )

class Question(BaseModelMixin):
    __tablename__ = "questions"

    quiz_id: Mapped[UUID] = mapped_column(ForeignKey('quizzes.id'), nullable=False)
    question_text: Mapped[str] = mapped_column(String(500))

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Answer(BaseModelMixin):
    __tablename__ = "answers"

    question_id: Mapped[UUID] = mapped_column(ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_text: Mapped[str] = mapped_column(String(500))
    is_correct: Mapped[bool] = mapped_column(default=False)

    question: Mapped["Question"] = relationship("Question", back_populates="answers")


class UserQuizAttempt(BaseModelMixin):
    __tablename__ = "user_quiz_attempts"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    quiz_id: Mapped[UUID] = mapped_column(ForeignKey("quizzes.id"), nullable=False)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)
    last_attempt_time: Mapped[datetime] = mapped_column(default=func.now())
    total_questions: Mapped[int] = mapped_column(default=0)
    correct_answers_count: Mapped[int] = mapped_column(default=0)


    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="user_attempts")
    company = relationship("Company", back_populates="quiz_attempts")