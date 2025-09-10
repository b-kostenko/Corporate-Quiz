from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.schemas.companies_schemas import CompanyOutputSchema, CompanyInputSchema
from app.core.schemas.pagination_schemas import PaginatedResponse, PaginationMeta
from app.infrastructure.postgres.models import Company, User
from app.utils.exceptions import ObjectAlreadyExists, ObjectNotFound


class CompanyService:
    def __init__(self, company_repository: AbstractCompanyRepository):
        self.company_repository: AbstractCompanyRepository = company_repository

    async def create(self, company_input: CompanyInputSchema, user: User) -> CompanyOutputSchema:
        company_instance = Company(**company_input.model_dump(), owner_id=user.id)
        company_exists = await self.company_repository.check_if_company_exists(
            company_email=company_instance.company_email, owner_id=user.id
        )
        if company_exists:
            raise ObjectAlreadyExists(message="Company with this email already exists.")
        created_company = await self.company_repository.create(company=company_instance)
        return CompanyOutputSchema.model_validate(created_company)

    async def update(self, company_id: int, user: User, company_input: CompanyInputSchema) -> CompanyOutputSchema:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        response = await self.company_repository.update(company=company, updates=company_input.model_dump())
        return CompanyOutputSchema.model_validate(response)

    async def delete(self, company_id: int, user: User) -> None:
        result = await self.company_repository.delete(company_id=company_id, owner_id=user.id)
        if not result:
            raise ObjectNotFound(model_name="Company", id_=company_id)

    async def get(self, company_id: int) -> CompanyOutputSchema | None:
        response = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not response:
            raise ObjectNotFound(model_name="Company", id_=company_id)
        return CompanyOutputSchema.model_validate(response)

    async def get_companies_for_owner(self, user: User) -> list[CompanyOutputSchema]:
        companies = await self.company_repository.get_companies_for_owner(owner_id=user.id)
        return [CompanyOutputSchema.model_validate(company) for company in companies]

    async def get_companies_for_owner_paginated(
        self, user: User, limit: int, offset: int
    ) -> PaginatedResponse[CompanyOutputSchema]:
        """Get paginated companies for owner."""
        companies, total = await self.company_repository.get_companies_for_owner_paginated(
            owner_id=user.id, limit=limit, offset=offset
        )
        
        # Convert to output schemas
        company_schemas = [CompanyOutputSchema.model_validate(company) for company in companies]
        
        # Create pagination metadata
        meta = PaginationMeta(
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
            has_previous=offset > 0
        )
        
        return PaginatedResponse[CompanyOutputSchema](items=company_schemas, meta=meta)

    async def change_status(self, company_id: int, user: User, company_status: str) -> CompanyOutputSchema:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        response = await self.company_repository.update(company=company, updates={"company_status": company_status})
        return CompanyOutputSchema.model_validate(response)

    async def upload_logo(self, company_id: int, user: User, company_logo: str) -> CompanyOutputSchema:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        response = await self.company_repository.update(company=company, updates={"company_logo_url": company_logo})
        return CompanyOutputSchema.model_validate(response)