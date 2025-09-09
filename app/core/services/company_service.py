from pydantic.v1 import UUID4

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.schemas.companies_schemas import CompanyOutputSchema, CompanyInputSchema
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

    async def update(self, company_id: int, company_input: CompanyInputSchema) -> CompanyOutputSchema:
        company = await self.company_repository.get(company_id=company_id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        response = await self.company_repository.update(company=company, updates=company_input.model_dump())
        return CompanyOutputSchema.model_validate(response)

    async def delete(self, company_id: int) -> None:
        await self.company_repository.delete(company_id=company_id)

    async def get(self, company_id: int) -> CompanyOutputSchema | None:
        response = await self.company_repository.get(company_id=company_id)
        if not response:
            raise ObjectNotFound(model_name="Company", id_=company_id)
        return CompanyOutputSchema.model_validate(response)

    async def get_companies_for_owner(self, user: User) -> list[CompanyOutputSchema]:
        companies = await self.company_repository.get_companies_for_owner(owner_id=user.id)
        return [CompanyOutputSchema.model_validate(company) for company in companies]