from abc import ABC, abstractmethod
from typing import Tuple

from pydantic import UUID4

from app.infrastructure.postgres.models import Company


class AbstractCompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> Company:
        raise NotImplementedError

    @abstractmethod
    async def get(self, company_id: int, owner_id: UUID4 | None = None) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def check_if_company_exists(self, company_email: str, owner_id: UUID4) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, company_id: int, owner_id: UUID4) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, company: Company, updates: dict) -> Company:
        raise NotImplementedError

    @abstractmethod
    async def get_companies_for_owner(self, owner_id: UUID4) -> list[Company]:
        raise NotImplementedError

    @abstractmethod
    async def get_companies_for_owner_paginated(
        self, owner_id: UUID4, limit: int, offset: int
    ) -> Tuple[list[Company], int]:
        """Get paginated companies for owner with total count."""
        raise NotImplementedError