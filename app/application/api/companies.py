from uuid import UUID

from fastapi import APIRouter, Query, UploadFile
from starlette import status

from app.application.api.deps import company_service_deps, current_user_deps, file_storage_deps
from app.core.schemas.company_schemas import (
    CompanyInputSchema,
    CompanyMemberOutputSchema,
    CompanyMemberUserSchema,
    CompanyOutputSchema,
    CompanyUpdateSchema,
)
from app.core.schemas.pagination_schemas import PaginatedResponse
from app.infrastructure.postgres.models.enums import CompanyMemberRole, CompanyStatus

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_input: CompanyInputSchema, user: current_user_deps, company_service: company_service_deps
) -> CompanyOutputSchema:
    """Create a new company."""
    company = await company_service.create(company_input=company_input, user=user)
    return company


@router.get("/all", response_model=PaginatedResponse[CompanyOutputSchema], status_code=status.HTTP_200_OK)
async def get_all_companies(
    limit: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    company_service: company_service_deps = None,
) -> PaginatedResponse[CompanyOutputSchema]:
    """Get paginated list of all companies."""
    companies = await company_service.get_all_companies_paginated(limit=limit, offset=offset)
    return companies


@router.get("/owned", response_model=PaginatedResponse[CompanyOutputSchema], status_code=status.HTTP_200_OK)
async def get_my_owned_companies(
    limit: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    user: current_user_deps = None,
    company_service: company_service_deps = None,
) -> PaginatedResponse[CompanyOutputSchema]:
    """Get paginated companies owned by the current user (where user is owner/admin)."""
    companies = await company_service.get_companies_for_owner_paginated(user=user, limit=limit, offset=offset)
    return companies


@router.get("/joined", response_model=PaginatedResponse[CompanyOutputSchema], status_code=status.HTTP_200_OK)
async def get_my_joined_companies(
    limit: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    user: current_user_deps = None,
    company_service: company_service_deps = None,
) -> PaginatedResponse[CompanyOutputSchema]:
    """Get paginated companies where the current user is a member (not owner)."""
    companies = await company_service.get_companies_for_member_paginated(user=user, limit=limit, offset=offset)
    return companies


@router.get("/{company_id}", response_model=CompanyMemberOutputSchema, status_code=status.HTTP_200_OK)
async def get_company(company_id: UUID, company_service: company_service_deps) -> CompanyMemberOutputSchema:
    """Get a company by its ID."""
    members = await company_service.get_company_members(company_id=company_id)
    return members


@router.put("/{company_id}", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def update_company(
    company_id: UUID, company_input: CompanyUpdateSchema, company_service: company_service_deps, user: current_user_deps
) -> CompanyOutputSchema:
    """Update a company by its ID."""
    company = await company_service.update(company_id=company_id, user=user, company_input=company_input)
    return company


@router.delete("/{company_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, company_service: company_service_deps, user: current_user_deps) -> None:
    """Delete a company by its ID."""
    await company_service.delete(company_id=company_id, user=user)


@router.patch("/{company_id}", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def change_company_status(
    company_id: UUID, company_status: CompanyStatus, company_service: company_service_deps, user: current_user_deps
) -> CompanyOutputSchema:
    """Change the status of a company by its ID."""
    company = await company_service.change_status(company_id=company_id, user=user, company_status=company_status)
    return company


@router.post("/{company_id}/logo", response_model=CompanyOutputSchema, status_code=status.HTTP_200_OK)
async def change_company_logo(
    company_id: UUID,
    logo_file: UploadFile,
    company_service: company_service_deps,
    user: current_user_deps,
    file_storage: file_storage_deps,
) -> CompanyOutputSchema:
    """Change the logo URL of a company by its ID."""
    content = await logo_file.read()
    company_logo = await file_storage.save_file(content=content, filename=logo_file.filename)
    company = await company_service.upload_logo(company_id=company_id, user=user, company_logo=company_logo)
    return company


@router.delete("/{company_id}/members/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def remove_company_member(
    company_id: UUID, user_id: UUID, company_service: company_service_deps, user: current_user_deps
) -> None:
    """Remove a member from a company."""
    await company_service.remove_user_from_company(company_id=company_id, user_id=user_id, user=user)


@router.patch(
    "/{company_id}/members/{user_id}/role", response_model=CompanyMemberUserSchema, status_code=status.HTTP_200_OK
)
async def change_company_member_role(
    company_id: UUID,
    user_id: UUID,
    new_role: CompanyMemberRole,
    company_service: company_service_deps,
    user: current_user_deps,
) -> CompanyMemberUserSchema:
    """Change a member's role in a company."""
    member = await company_service.change_member_role(
        company_id=company_id, user_id=user_id, new_role=new_role, user=user
    )
    return member


@router.get("/{company_id}/admins", response_model=list[CompanyMemberUserSchema], status_code=status.HTTP_200_OK)
async def get_company_admins(
    company_id: UUID, user: current_user_deps = None, company_service: company_service_deps = None
) -> list[CompanyMemberUserSchema]:
    """Get all admins of a specific company."""
    admins = await company_service.get_company_admins(company_id=company_id, user=user)
    return admins
