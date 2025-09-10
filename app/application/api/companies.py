
from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import UUID4
from starlette import status

from app.application.api.deps import current_user_deps, company_deps, file_storage_deps
from app.core.interfaces.file_storage_interface import FileStorageInterface
from app.core.schemas.companies_schemas import CompanyOutputSchema, CompanyInputSchema, CompanyUpdateSchema, \
    CompanyStatus

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
async def update_company(company_id: UUID4, company_input: CompanyUpdateSchema, company_service: company_deps, user: current_user_deps) -> CompanyOutputSchema:
    """Update a company by its ID."""
    company = await company_service.update(company_id=company_id, user=user, company_input=company_input)
    return company

@router.delete("/{company_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID4, company_service: company_deps, user: current_user_deps) -> None:
    """Delete a company by its ID."""
    await company_service.delete(company_id=company_id, user=user)

@router.patch("/{company_id}", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def change_company_status(company_id: UUID4, company_status: CompanyStatus, company_service: company_deps, user: current_user_deps) -> CompanyOutputSchema:
    """Change the status of a company by its ID."""
    company = await company_service.change_status(company_id=company_id, user=user, company_status=company_status)
    return company


@router.post("/{company_id}/logo", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def change_company_logo(
    company_id: UUID4, 
    logo_file: UploadFile, 
    company_service: company_deps, 
    user: current_user_deps,
    file_storage: file_storage_deps
) -> CompanyOutputSchema:
    """Change the logo URL of a company by its ID."""
    if not logo_file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    content = await logo_file.read()
    company_logo = await file_storage.save_file(content=content, filename=logo_file.filename)
    company = await company_service.upload_logo(company_id=company_id, user=user, company_logo=company_logo)
    return company
