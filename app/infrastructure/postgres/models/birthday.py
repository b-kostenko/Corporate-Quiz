from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.postgres.models.base import BaseModelMixin


class Birthday(BaseModelMixin):
    __tablename__ = "birthdays"

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    person_name: Mapped[str] = mapped_column(String(200), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
