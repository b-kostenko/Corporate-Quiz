from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.postgres.models import User
from app.infrastructure.postgres.models.base import BaseModelMixin
from app.infrastructure.postgres.models.enums import CompanyMemberRole, CompanyStatus, InvitationStatus


class Company(BaseModelMixin):
    __tablename__ = "companies"

    company_name: Mapped[str] = mapped_column(String(100))
    company_address: Mapped[str] = mapped_column(String(200))
    company_email: Mapped[str] = mapped_column(String(200))
    company_phone: Mapped[str | None] = mapped_column(String(15))
    company_website: Mapped[str | None] = mapped_column(String(200))
    company_logo_url: Mapped[str | None] = mapped_column(String(200))
    company_description: Mapped[str | None] = mapped_column(String(500))
    company_status: Mapped[CompanyStatus] = mapped_column(
        Enum(CompanyStatus, native_enum=False), default=CompanyStatus.VISIBLE, nullable=False
    )
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped[User] = relationship(User)

    quiz_attempts = relationship("UserQuizAttempt", back_populates="company")

    __table_args__ = (UniqueConstraint("owner_id", "company_email", name="uq_owner_email"),)


class CompanyMember(BaseModelMixin):
    __tablename__ = "company_members"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    role: Mapped[CompanyMemberRole] = mapped_column(
        Enum(CompanyMemberRole, native_enum=False), default=CompanyMemberRole.MEMBER, nullable=False
    )


class CompanyInvitation(BaseModelMixin):
    __tablename__ = "company_invitations"

    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"))
    invited_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    invited_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    status: Mapped[InvitationStatus] = mapped_column(
        Enum(InvitationStatus, native_enum=False), default=InvitationStatus.PENDING, nullable=False
    )
