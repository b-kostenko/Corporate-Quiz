
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from sqlalchemy import String, Date

from app.infrastructure.postgres.models.base import BaseModelMixin


class User(BaseModelMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime | None] = mapped_column(Date)
    avatar_url: Mapped[str | None] = mapped_column(String(200))
