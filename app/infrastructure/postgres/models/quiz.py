from uuid import UUID

from sqlalchemy import String, ForeignKey
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
        lazy="selectin"
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

    question_id: Mapped[UUID] = mapped_column(ForeignKey('questions.id'), nullable=False)
    answer_text: Mapped[str] = mapped_column(String(500))
    is_correct: Mapped[bool] = mapped_column(default=False)

    question: Mapped["Question"] = relationship("Question", back_populates="answers")