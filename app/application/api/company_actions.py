from fastapi import APIRouter
from pydantic import UUID4
from starlette import status

from app.application.api.deps import company_service_deps, current_user_deps, user_service_deps
from app.core.schemas.companies_schemas import CompanyInvitationInputSchema, \
    CompanyInvitationOutputSchema

router = APIRouter(prefix="/company-actions", tags=["Company Actions"])


@router.post("/invite", response_model=CompanyInvitationOutputSchema, status_code=status.HTTP_200_OK)
async def invite_user_to_company(
        payload: CompanyInvitationInputSchema,
        company_service: company_service_deps,
        user_service: user_service_deps,
        user: current_user_deps
):
    """Invite a user to a company."""
    invite_user = await user_service.get(email=payload.invite_user_email)
    invite = await company_service.invite_user_to_company(company_id=payload.company_id, invite_user=invite_user, user=user)
    return invite


@router.post("/accept-invitation/{invitation_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def accept_company_invitation(
        invitation_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Accept a company invitation."""
    await company_service.accept_company_invitation(invitation_id=invitation_id, user=user)

@router.post("/decline-invitation/{invitation_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def decline_company_invitation(
        invitation_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Decline a company invitation."""
    await company_service.decline_company_invitation(invitation_id=invitation_id, user=user)

@router.post("/cancel-invitation/{invitation_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def cancel_company_invitation(
        invitation_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Cancel a company invitation."""
    await company_service.cancel_company_invitation(invitation_id=invitation_id, user=user)


@router.get("/invitations", response_model=list[CompanyInvitationOutputSchema], status_code=status.HTTP_200_OK)
async def get_my_invitations(
        company_service: company_service_deps,
        user: current_user_deps
):
    """Get all invitations for the current user."""
    invitations = await company_service.get_invitations_for_user(user=user)
    return invitations

@router.get("/company-invitations", response_model=list[CompanyInvitationOutputSchema], status_code=status.HTTP_200_OK)
async def get_company_invitations(
        company_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Get all invitations for a specific company."""
    invitations = await company_service.get_invitations_for_company(company_id=company_id, user=user)
    return invitations

@router.post("/{company_id}/membership-requests", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def request_membership_to_company(
        company_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Request membership to a company."""
    await company_service.request_membership_to_company(company_id=company_id, user=user)


@router.post("/{company_id}/membership-leave", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def leave_company(
        company_id: UUID4,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Leave a company."""
    await company_service.leave_company(company_id=company_id, user=user)