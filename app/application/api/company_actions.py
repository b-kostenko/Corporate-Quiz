from uuid import UUID

from fastapi import APIRouter
from starlette import status

from app.application.api.deps import company_service_deps, current_user_deps, user_service_deps
from app.core.schemas.company_schemas import CompanyInvitationInputSchema, CompanyInvitationOutputSchema
from app.infrastructure.postgres.models.enums import InvitationType

router = APIRouter(prefix="/company-actions", tags=["Company Actions"])



@router.get("/{company_id}/company-invitations", response_model=list[CompanyInvitationOutputSchema], status_code=status.HTTP_200_OK)
async def get_company_invitations(
        company_id: UUID,
        company_service: company_service_deps,
        user: current_user_deps
):
    """Get all invitations for a specific company."""
    invitations = await company_service.get_invitations_for_company(company_id=company_id, user=user)
    return invitations


@router.post("/invite", response_model=CompanyInvitationOutputSchema, status_code=status.HTTP_200_OK)
async def invite_user_to_company(
    payload: CompanyInvitationInputSchema,
    company_service: company_service_deps,
    user_service: user_service_deps,
    user: current_user_deps,
):
    """Invite a user to a company."""
    invite_user = await user_service.get(email=payload.invite_user_email)
    await company_service.check_if_user_is_invited(
        company_id=payload.company_id, invite_user=invite_user
    )
    invite = await company_service.invite_user_to_company(
        company_id=payload.company_id, invite_user=invite_user, user=user
    )
    return invite


@router.post("/{invitation_id}/accept", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def accept_incoming_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Accept a user's request to join the company."""
    await company_service.accept_incoming_user_invitation(invitation_id=invitation_id, user=user)


@router.post("/{invitation_id}/reject", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def reject_incoming_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Reject a company invitation."""
    await company_service.reject_incoming_user_invitation(invitation_id=invitation_id, user=user)


@router.post("/{invitation_id}/cancel", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def cancel_outgoing_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Cancel a company invitation."""
    await company_service.cancel_outgoing_user_invitation(invitation_id=invitation_id, user=user)
