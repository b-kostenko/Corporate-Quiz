from pydantic import UUID4

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.core.schemas.companies_schemas import CompanyOutputSchema, CompanyInputSchema, InvitationStatus, \
    CompanyMemberOutputSchema
from app.core.schemas.pagination_schemas import PaginatedResponse, PaginationMeta
from app.core.schemas.user_schemas import UserOutputSchema
from app.infrastructure.postgres.models import Company, User
from app.infrastructure.postgres.models.company import CompanyInvitation
from app.utils.exceptions import ObjectAlreadyExists, ObjectNotFound, UnauthorizedAction


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

    async def get_all_companies_paginated(self, limit: int, offset: int) -> PaginatedResponse[CompanyOutputSchema]:
        """Get paginated list of all companies."""
        # Assuming the repository has a method to get all companies with pagination
        companies, total = await self.company_repository.get_all_companies_paginated(limit=limit, offset=offset)

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

    async def invite_user_to_company(self,company_id: UUID4, invite_user: User, user: User) -> CompanyInvitation:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        invite_exists = await self.company_repository.check_if_invite_exists(
            company=company, invite_user=invite_user, status=InvitationStatus.PENDING
        )
        if invite_exists:
            raise ObjectAlreadyExists(message="User is already invited or a member of the company.")

        invited = await self.company_repository.invite_user_to_company(
            company=company, invite_user=invite_user, invited_by=user
        )
        return invited

    async def accept_company_invitation(self, invitation_id: UUID4, user: User) -> None:
        invitation = await self.company_repository.get_invitation_by_id(invitation_id=invitation_id)
        company = await self.company_repository.get(company_id=invitation.company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=invitation.company_id)

        if not invitation:
            raise ObjectNotFound(model_name="Company Invitation", id_=invitation_id)

        if invitation.status != InvitationStatus.PENDING:
            raise ObjectAlreadyExists(message="Invitation has already been responded to.")

        await self.company_repository.accept_company_invitation(invitation=invitation)

        await self.company_repository.add_user_to_company(
            company=company, user_id=invitation.invited_user_id
        )


    async def decline_company_invitation(self, invitation_id: UUID4, user: User) -> None:
        invitation = await self.company_repository.get_invitation_by_id(invitation_id=invitation_id)
        if not invitation:
            raise ObjectNotFound(model_name="Company Invitation", id_=invitation_id)

        if invitation.status != InvitationStatus.PENDING:
            raise ObjectAlreadyExists(message="Invitation has already been responded to.")

        if invitation.invited_by_id != user.id:
            raise UnauthorizedAction(message="You are not authorized to decline this invitation.")

        await self.company_repository.decline_company_invitation(invitation=invitation)

    async def cancel_company_invitation(self, invitation_id: UUID4, user: User) -> None:
        invitation = await self.company_repository.get_invitation_by_id(invitation_id=invitation_id)
        if not invitation:
            raise ObjectNotFound(model_name="Company Invitation", id_=invitation_id)

        if invitation.invited_by_id != user.id:
            raise UnauthorizedAction(message="You are not authorized to decline this invitation.")

        await self.company_repository.cancel_company_invitation(invitation=invitation)


    async def get_invitations_for_user(self, user: User) -> list[CompanyInvitation]:
        invitations = await self.company_repository.get_invitations_for_user(user=user)
        return invitations

    async def get_invitations_for_company(self, company_id: UUID4, user: User) -> list[CompanyInvitation]:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        invitations = await self.company_repository.get_invitations_for_company(company=company)
        return invitations

    async def request_membership_to_company(self, company_id: UUID4, user: User) -> None:
        company = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        invite_exists = await self.company_repository.check_if_invite_exists(
            company=company, invite_user=user, status=InvitationStatus.PENDING
        )
        if invite_exists:
            raise ObjectAlreadyExists(message="You have already requested membership or are a member of the company.")

        await self.company_repository.invite_user_to_company(
            company=company, invite_user=user, invited_by=user
        )

    async def leave_company(self, company_id: UUID4, user: User) -> None:
        company = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        user_is_company_member = await self.company_repository.check_if_user_is_company_member(company=company, user_id=user.id)
        if not user_is_company_member:
            raise ObjectNotFound(model_name="Company Member", id_=user.id)

        await self.company_repository.remove_user_from_company(company=company, user_id=user.id, user=user)

    async def get_company_members(self, company_id: UUID4) -> CompanyMemberOutputSchema:
        """Get paginated list of all companies."""
        company = await self.company_repository.get(company_id=company_id, owner_id=None)
        if not company:
            raise ObjectNotFound(model_name="Company Invitation", id_=company_id)

        # Assuming the repository has a method to get all companies with pagination
        members = await self.company_repository.get_company_members(company=company)

        user_schemas = [UserOutputSchema.model_validate(user) for user in members]

        company_schema = CompanyMemberOutputSchema.model_validate({
            **CompanyOutputSchema.model_validate(company).model_dump(),
            "users": user_schemas
        })
        return company_schema

    async def remove_user_from_company(self, company_id: UUID4, user_id: UUID4, user: User) -> None:
        company = await self.company_repository.get(company_id=company_id, owner_id=user.id)
        if not company:
            raise ObjectNotFound(model_name="Company", id_=company_id)

        user_is_company_member = await self.company_repository.check_if_user_is_company_member(company=company, user_id=user_id)
        if not user_is_company_member:
            raise ObjectNotFound(model_name="Company Member", id_=user_id)

        await self.company_repository.remove_user_from_company(company=company, user_id=user_id, user=user)