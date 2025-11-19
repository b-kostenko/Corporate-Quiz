from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.core.schemas.user_schemas import UserOutputSchema
from app.infrastructure.postgres.models import CompanyMember, User
from app.infrastructure.postgres.models.enums import CompanyMemberRole, CompanyStatus, InvitationStatus, InvitationType


class CompanyInputSchema(BaseModel):
    """Schema for company input data."""

    company_name: str
    company_address: str
    company_email: EmailStr
    company_phone: str | None = None
    company_website: str | None = None
    company_logo_url: str | None = None
    company_description: str | None = None
    company_status: CompanyStatus


class CompanyOutputSchema(BaseModel):
    """Schema for company output data."""

    id: UUID
    company_name: str
    company_address: str
    company_email: EmailStr
    company_phone: str | None = None
    company_website: str | None = None
    company_logo_url: str | None = None
    company_description: str | None = None
    company_status: CompanyStatus

    class Config:
        from_attributes = True


class CompanyUpdateSchema(BaseModel):
    """Schema for updating company data."""

    company_name: str | None = None
    company_description: str | None = None
    company_address: str | None = None
    company_phone: str | None = None
    company_website: str | None = None


class CompanyInvitationInputSchema(BaseModel):
    """Schema for company invitation input data."""

    company_id: UUID
    invite_user_email: EmailStr


class CompanyInvitationOutputSchema(BaseModel):
    """Schema for company invitation data."""

    id: UUID
    company: CompanyOutputSchema
    invited_user: UserOutputSchema
    invited_by: UserOutputSchema
    invitation_type: InvitationType
    status: InvitationStatus

    class Config:
        from_attributes = True


class CompanyMemberUserSchema(BaseModel):
    """Schema for company member user with role."""

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar_url: str | None = None
    role: CompanyMemberRole

    class Config:
        from_attributes = True

    @classmethod
    def from_models(cls, user: User, company_member: CompanyMember) -> "CompanyMemberUserSchema":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            avatar_url=user.avatar_url,
            role=company_member.role,
        )


class CompanyMemberOutputSchema(CompanyOutputSchema):
    """Schema for company member output data."""

    owner: CompanyMemberUserSchema | None = None
    members: list[CompanyMemberUserSchema] = []
