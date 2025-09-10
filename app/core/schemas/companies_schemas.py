from enum import StrEnum

from pydantic import BaseModel, EmailStr, UUID4

from app.core.schemas.user_schemas import UserOutputSchema


class CompanyStatus(StrEnum):
    HIDDEN = "hidden"
    VISIBLE = "visible"


class CompanyMemberRole(StrEnum):
    MEMBER = "member"
    SUPPORT = "support"
    ADMIN = "admin"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELED = "canceled"


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

    id: UUID4
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

    company_id: UUID4
    invite_user_email: EmailStr


class CompanyInvitationOutputSchema(BaseModel):
    """Schema for company invitation data."""

    id: UUID4
    company_id: UUID4
    invited_user_id: UUID4
    invited_by_id: UUID4
    status: InvitationStatus

    class Config:
        from_attributes = True


class CompanyMemberOutputSchema(CompanyOutputSchema):
    """Schema for company member output data."""

    users: list[UserOutputSchema]
