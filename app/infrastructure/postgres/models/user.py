from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.postgres.models.base import BaseModelMixin


class User(BaseModelMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[EmailStr] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    avatar_url: Mapped[str | None] = mapped_column(String(200))
