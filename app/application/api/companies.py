
from fastapi import APIRouter
from pydantic import UUID4
from starlette import status

from app.application.api.deps import current_user_deps, company_deps
from app.core.schemas.companies_schemas import CompanyOutputSchema, CompanyInputSchema, CompanyUpdateSchema

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_company(company_input: CompanyInputSchema, user: current_user_deps, company_service: company_deps) -> CompanyOutputSchema:
    """Create a new company."""
    company = await company_service.create(company_input=company_input, user=user)
    return company

@router.get("/", response_model=list[CompanyOutputSchema], status_code=status.HTTP_200_OK)
async def get_my_companies(user: current_user_deps, company_service: company_deps) -> list[CompanyOutputSchema]:
    """Get all companies for the current user."""
    companies = await company_service.get_companies_for_owner(user=user)
    return companies

@router.get("/{company_id}", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def get_company(company_id: UUID4, company_service: company_deps) -> CompanyOutputSchema:
    """Get a company by its ID."""
    company = await company_service.get(company_id=company_id)
    return company

@router.put("/{company_id}", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def update_company(company_id: UUID4, company_input: CompanyUpdateSchema, company_service: company_deps) -> CompanyOutputSchema:
    """Update a company by its ID."""
    company = await company_service.update(company_id=company_id, company_input=company_input)
    return company

@router.delete("/{company_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID4, company_service: company_deps) -> None:
    """Delete a company by its ID."""
    await company_service.delete(company_id=company_id)