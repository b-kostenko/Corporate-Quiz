from typing import Sequence

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.infrastructure.postgres.models import Company
from app.infrastructure.postgres.session_manager import provide_async_session


class CompanyRepository(AbstractCompanyRepository):
    @provide_async_session
    async def create(self, company: Company, session: AsyncSession) -> Company:
        session.add(company)
        await session.commit()
        await session.refresh(company)
        return company

    @provide_async_session
    async def check_if_company_exists(self, company_email: str, owner_id: UUID4, session: AsyncSession) -> Company | None:
        query = select(Company).where(Company.company_email == company_email, Company.owner_id == owner_id)
        company = await session.execute(query)
        return company.scalar_one_or_none()

    @provide_async_session
    async def get(self, company_id: int, owner_id: UUID4 | None, session: AsyncSession) -> Company | None:
        constraints = [Company.id == company_id]
        if owner_id:
            constraints.append(Company.owner_id == owner_id)
        query = select(Company).where(*constraints)
        company = await session.execute(query)
        return company.scalar_one_or_none()

    @provide_async_session
    async def update(self, company: Company, updates: dict, session: AsyncSession) -> Company:
        company = await session.merge(company)
        for key, value in updates.items():
            if value is not None:
                setattr(company, key, value)
        await session.commit()
        await session.refresh(company)
        return company

    @provide_async_session
    async def get_companies_for_owner(self, owner_id: UUID4, session: AsyncSession) -> Sequence[Company]:
        query = select(Company).where(Company.owner_id == owner_id)
        result = await session.execute(query)
        return result.scalars().all()

    @provide_async_session
    async def delete(self, company_id: int, owner_id: UUID4, session: AsyncSession) -> bool:
        company = await self.get(company_id=company_id, owner_id=owner_id)
        if not company:
            return False

        await session.delete(company)
        await session.commit()
        return True

