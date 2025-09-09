from uuid import UUID
from sqlalchemy import String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.schemas.companies_schemas import CompanyStatus
from app.infrastructure.postgres.models import User
from app.infrastructure.postgres.models.base import BaseModelMixin


class Company(BaseModelMixin):
    __tablename__ = "companies"

    company_name : Mapped[str] = mapped_column(String(100))
    company_address : Mapped[str] = mapped_column(String(200))
    company_email : Mapped[str] = mapped_column(String(200))
    company_phone : Mapped[str | None] = mapped_column(String(15))
    company_website : Mapped[str | None] = mapped_column(String(200))
    company_logo_url : Mapped[str | None] = mapped_column(String(200))
    company_description : Mapped[str | None] = mapped_column(String(500))
    company_status: Mapped[CompanyStatus] = mapped_column(
        Enum(CompanyStatus, native_enum=False),
        default=CompanyStatus.VISIBLE,
        nullable=False
    )
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner: Mapped[User] = relationship(User)

    __table_args__ = (
        UniqueConstraint("owner_id", "company_email", name="uq_owner_email"),
    )


