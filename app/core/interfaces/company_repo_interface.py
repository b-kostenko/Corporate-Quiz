from abc import ABC, abstractmethod
from typing import Tuple, Sequence

from pydantic import UUID4

from app.core.schemas.companies_schemas import InvitationStatus
from app.infrastructure.postgres.models import Company, User
from app.infrastructure.postgres.models.company import CompanyInvitation, CompanyMember


class AbstractCompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> Company:
        raise NotImplementedError

    @abstractmethod
    async def get(self, company_id: UUID4, owner_id: UUID4 | None = None) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def check_if_company_exists(self, company_email: str, owner_id: UUID4) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, company_id: UUID4, owner_id: UUID4) -> None:
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

    @abstractmethod
    async def get_all_companies_paginated(self, limit: int, offset: int) -> Tuple[list[Company], int]:
        """Get paginated companies with total count."""
        raise NotImplementedError

    @abstractmethod
    async def invite_user_to_company(self, company: Company, invite_user: User, invited_by: User) -> CompanyInvitation:
        """Invite a user to a company."""
        raise NotImplementedError

    @abstractmethod
    async def check_if_invite_exists(self, company: Company, invite_user: User, status: InvitationStatus) -> Company | None:
        """Check if an invitation to a user for a specific company already exists."""
        raise NotImplementedError

    @abstractmethod
    async def get_invitation_by_id(self, invitation_id: UUID4) -> CompanyInvitation | None:
        """Get invitation by ID."""
        raise NotImplementedError

    @abstractmethod
    async def accept_company_invitation(self, invitation: CompanyInvitation) -> None:
        """Get invitation by ID."""
        raise NotImplementedError

    @abstractmethod
    async def decline_company_invitation(self, invitation: CompanyInvitation) -> None:
        """Get invitation by ID."""
        raise NotImplementedError

    @abstractmethod
    async def add_user_to_company(self, company: Company, user_id: UUID4) -> None:
        """Get invitation by ID."""
        raise NotImplementedError

    @abstractmethod
    async def cancel_company_invitation(self, invitation: CompanyInvitation) -> None:
        """Get invitation by ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_company_members(self, company: Company, ) -> Sequence[User]:
        """Get paginated company members with total count."""
        raise NotImplementedError

    @abstractmethod
    async def get_invitations_for_user(self, user: User) -> list[CompanyInvitation]:
        """Get all invitations for a user."""
        raise NotImplementedError

    @abstractmethod
    async def get_invitations_for_company(self, company: Company) -> list[CompanyInvitation]:
        """Get all invitations for a specific company."""
        raise NotImplementedError

    @abstractmethod
    async def remove_user_from_company(self, company: Company, user_id: UUID4, user: User) -> None:
        """ Remove a user from a company."""
        raise NotImplementedError

    @abstractmethod
    async def check_if_user_is_company_member(self, company: Company, user_id: UUID4) -> bool:
        """ Check if a user is a member of a company."""
        raise NotImplementedError