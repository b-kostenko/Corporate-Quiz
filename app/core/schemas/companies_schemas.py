from enum import StrEnum

from pydantic import BaseModel, EmailStr, UUID4

class CompanyStatus(StrEnum):
    HIDDEN = "hidden"
    VISIBLE = "visible"

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