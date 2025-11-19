from uuid import UUID

from fastapi import APIRouter
from starlette import status

from app.application.api.deps import company_service_deps, current_user_deps
from app.core.schemas.company_schemas import CompanyInvitationOutputSchema

router = APIRouter(prefix="/user-actions", tags=["User Actions"])


@router.get("/invitations", response_model=list[CompanyInvitationOutputSchema], status_code=status.HTTP_200_OK)
async def get_my_invitations(company_service: company_service_deps, user: current_user_deps):
    """Get all invitations for the current user."""
    invitations = await company_service.get_invitations_for_user(user=user)
    return invitations

@router.post("/{company_id}/requests", response_model=CompanyInvitationOutputSchema, status_code=status.HTTP_201_CREATED)
async def request_membership_to_company(
    company_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Request membership to a company."""
    invitations = await company_service.request_membership_to_company(company_id=company_id, user=user)
    return invitations

@router.post("/{invitation_id}/accept", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def accept_incoming_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Accept invitation from a company."""
    await company_service.accept_incoming_company_invitation(invitation_id=invitation_id, user=user)

@router.post("/{invitation_id}/reject", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def reject_incoming_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Reject invitation from a company."""
    await company_service.reject_incoming_company_invitation(invitation_id=invitation_id, user=user)

@router.post("/{invitation_id}/cancel", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def cancel_outgoing_invitation(
    invitation_id: UUID, company_service: company_service_deps, user: current_user_deps
):
    """Cancel my outgoing membership request to a company."""
    await company_service.cancel_outgoing_company_request(invitation_id=invitation_id, user=user)

@router.post("/{company_id}/leave", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def leave_from_company(company_id: UUID, company_service: company_service_deps, user: current_user_deps):
    """Leave a company."""
    await company_service.leave_company(company_id=company_id, user=user)