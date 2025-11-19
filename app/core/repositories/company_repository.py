from typing import Sequence, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.interfaces.company_repo_interface import AbstractCompanyRepository
from app.infrastructure.postgres.models import Company, User
from app.infrastructure.postgres.models.company import CompanyInvitation, CompanyMember
from app.infrastructure.postgres.models.enums import CompanyMemberRole, InvitationStatus, CompanyStatus, InvitationType
from app.infrastructure.postgres.session_manager import provide_async_session


class CompanyRepository(AbstractCompanyRepository):
    @provide_async_session
    async def create(self, company: Company, session: AsyncSession) -> Company:
        session.add(company)
        await session.commit()
        await session.refresh(company)
        return company

    @provide_async_session
    async def check_if_company_exists(
        self, company_email: str, owner_id: UUID, session: AsyncSession
    ) -> Company | None:
        query = select(Company).where(Company.company_email == company_email, Company.owner_id == owner_id)
        company = await session.execute(query)
        return company.scalar_one_or_none()

    @provide_async_session
    async def get(self, company_id: int, owner_id: UUID | None, session: AsyncSession) -> Company | None:
        constraints = [Company.id == company_id]
        if owner_id:
            constraints.append(Company.owner_id == owner_id)

        query = (
            select(Company)
            .options(selectinload(Company.members))
            .where(*constraints)
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()

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
    async def get_companies_for_owner(self, owner_id: UUID, session: AsyncSession) -> Sequence[Company]:
        query = select(Company).where(Company.owner_id == owner_id)
        result = await session.execute(query)
        return result.scalars().all()

    @provide_async_session
    async def get_companies_for_owner_paginated(
        self, owner_id: UUID, limit: int, offset: int, session: AsyncSession
    ) -> Tuple[list[Company], int]:
        """Get paginated companies for owner with total count."""
        # Get total count
        count_query = select(func.count(Company.id)).where(Company.owner_id == owner_id)
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = (
            select(Company)
            .where(Company.owner_id == owner_id)
            .order_by(Company.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        companies = result.scalars().all()

        return list(companies), total

    @provide_async_session
    async def delete(self, company: Company, owner_id: UUID, session: AsyncSession) -> bool:
        await session.delete(company)
        await session.commit()
        return True

    @provide_async_session
    async def get_all_companies_paginated(
        self, limit: int, offset: int, session: AsyncSession
    ) -> Tuple[list[Company], int]:
        """Get paginated companies with total count."""
        # Get total count
        count_query = select(func.count(Company.id))
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = select(Company).where(Company.company_status == CompanyStatus.VISIBLE).order_by(Company.created_at.desc()).limit(limit).offset(offset)
        result = await session.execute(query)
        companies = result.scalars().all()

        return list(companies), total

    @provide_async_session
    async def invite_user_to_company(
        self, company: Company, invite_user: User, invited_by: User, invitation_type: InvitationType, session: AsyncSession
    ) -> CompanyInvitation:
        query = {
            "company_id": company.id,
            "invited_user_id": invite_user.id,
            "invited_by_id": invited_by.id,
            "invitation_type": invitation_type
        }
        invitation = CompanyInvitation(**query)
        session.add(invitation)
        await session.commit()
        await session.refresh(invitation)
        return invitation

    @provide_async_session
    async def check_if_invite_exists(
        self, company: Company, invite_user: User, status: InvitationStatus, session: AsyncSession
    ) -> CompanyInvitation | None:
        query = select(CompanyInvitation).where(
            CompanyInvitation.company_id == company.id,
            CompanyInvitation.invited_user_id == invite_user.id,
            CompanyInvitation.status == status,
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @provide_async_session
    async def get_invitation_by_id(self, invitation_id: UUID, session: AsyncSession) -> CompanyInvitation | None:
        query = select(CompanyInvitation).where(
            CompanyInvitation.id == invitation_id, CompanyInvitation.status == InvitationStatus.PENDING
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @provide_async_session
    async def add_user_to_company(
        self, company: Company, user_id: UUID, role: CompanyMemberRole, session: AsyncSession
    ) -> None:
        query = {"company_id": company.id, "user_id": user_id, "role": role}
        company_member = CompanyMember(**query)
        session.add(company_member)
        await session.commit()
        await session.refresh(company_member)

    @provide_async_session
    async def get_company_members(
        self, company: Company, session: AsyncSession
    ) -> Sequence[tuple[User, CompanyMember]]:
        """Get users of a company with their membership information.

        Returns:
            Sequence of tuples containing (User, CompanyMember) pairs,
            where User contains user data and CompanyMember contains role and membership info.
        """
        query = (
            select(User, CompanyMember)
            .join(CompanyMember, CompanyMember.user_id == User.id)
            .where(CompanyMember.company_id == company.id)
            .order_by(CompanyMember.created_at.desc())
        )
        result = await session.execute(query)
        user_member_pairs = result.all()

        return user_member_pairs

    @provide_async_session
    async def get_company_member(self, company: Company, user_id: UUID, session: AsyncSession) -> CompanyMember | None:
        """Get a specific company member."""
        query = select(CompanyMember).where(CompanyMember.company_id == company.id, CompanyMember.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @provide_async_session
    async def get_invitations_for_user(
        self, user: User, session: AsyncSession
    ) -> Sequence[CompanyInvitation]:
        """Get all invitations for a user with loaded relationships."""
        stmt = (
            select(CompanyInvitation)
            .where(CompanyInvitation.invited_user_id == user.id)
            .options(
                selectinload(CompanyInvitation.company),
                selectinload(CompanyInvitation.invited_user),
                selectinload(CompanyInvitation.invited_by)
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @provide_async_session
    async def get_invitations_for_company(
        self, company: Company, session: AsyncSession
    ) -> Sequence[CompanyInvitation]:
        """Get all invitations for a company with loaded relationships."""
        stmt = (
            select(CompanyInvitation)
            .where(CompanyInvitation.company_id == company.id)
            .options(
                selectinload(CompanyInvitation.company),
                selectinload(CompanyInvitation.invited_user),
                selectinload(CompanyInvitation.invited_by)
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @provide_async_session
    async def check_if_user_is_company_member(self, company: Company, user_id: UUID, session: AsyncSession) -> bool:
        query = select(CompanyMember).where(CompanyMember.company_id == company.id, CompanyMember.user_id == user_id)

        result = await session.execute(query)
        company_member = result.scalar_one_or_none()
        return company_member is not None

    @provide_async_session
    async def remove_user_from_company(
        self, company: Company, user_id: UUID, session: AsyncSession
    ) -> None:
        query = select(CompanyMember).where(CompanyMember.company_id == company.id, CompanyMember.user_id == user_id)
        result = await session.execute(query)
        company_member = result.scalar_one_or_none()

        await session.delete(company_member)
        await session.commit()

    @provide_async_session
    async def change_member_role(
        self, company: Company, user_id: UUID, new_role: CompanyMemberRole, session: AsyncSession
    ) -> tuple[User, CompanyMember] | None:
        query = (
            select(User, CompanyMember)
            .join(CompanyMember, CompanyMember.user_id == User.id)
            .where(CompanyMember.company_id == company.id, CompanyMember.user_id == user_id)
        )
        result = await session.execute(query)
        user, company_member = result.one_or_none()
        company_member.role = new_role
        await session.commit()
        await session.refresh(company_member)
        return user, company_member

    @provide_async_session
    async def remove_user_invitations(self, company: Company, user_id: UUID, session: AsyncSession) -> None:
        query = select(CompanyInvitation).where(
            CompanyInvitation.company_id == company.id,
            CompanyInvitation.invited_user_id == user_id
        )
        result = await session.execute(query)
        invitations = result.scalars().all()

        for invitation in invitations:
            await session.delete(invitation)

        await session.commit()

    @provide_async_session
    async def get_companies_for_member(self, user_id: UUID, session: AsyncSession) -> Sequence[Company]:
        """Get companies where user is a member (not owner)."""
        query = (
            select(Company)
            .join(CompanyMember, CompanyMember.company_id == Company.id)
            .where(CompanyMember.user_id == user_id, Company.owner_id != user_id)
            .order_by(Company.created_at.desc())
        )
        result = await session.execute(query)
        return result.scalars().all()

    @provide_async_session
    async def get_companies_for_member_paginated(
        self, user_id: UUID, limit: int, offset: int, session: AsyncSession
    ) -> Tuple[list[Company], int]:
        """Get paginated companies where user is a member (not owner) with total count."""
        # Get total count
        count_query = (
            select(func.count(Company.id))
            .join(CompanyMember, CompanyMember.company_id == Company.id)
            .where(CompanyMember.user_id == user_id, Company.owner_id != user_id)
        )
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = (
            select(Company)
            .join(CompanyMember, CompanyMember.company_id == Company.id)
            .where(CompanyMember.user_id == user_id, Company.owner_id != user_id)
            .order_by(Company.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        companies = result.scalars().all()

        return list(companies), total

    @provide_async_session
    async def cancel_invitation(self, invitation: CompanyInvitation, session: AsyncSession):
        invitation = await session.merge(invitation)
        invitation.status = InvitationStatus.CANCELED
        await session.commit()
        await session.refresh(invitation)


    @provide_async_session
    async def accept_invitation(self, invitation: CompanyInvitation, session: AsyncSession) -> None:
        invitation = await session.merge(invitation)
        invitation.status = InvitationStatus.ACCEPTED
        await session.commit()
        await session.refresh(invitation)

    @provide_async_session
    async def reject_invitation(self, invitation: CompanyInvitation, session: AsyncSession) -> None:
        invitation = await session.merge(invitation)
        invitation.status = InvitationStatus.REJECTED
        await session.commit()
        await session.refresh(invitation)

    @provide_async_session
    async def decline_invitation(self, invitation: CompanyInvitation, session: AsyncSession) -> None:
        invitation = await session.merge(invitation)
        invitation.status = InvitationStatus.DECLINED
        await session.commit()
        await session.refresh(invitation)