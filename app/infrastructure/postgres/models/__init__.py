from app.infrastructure.postgres import DeclarativeBase
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from sqlalchemy import func


class BaseModelMixin(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now(), server_default=func.now())
