from enum import StrEnum


class CompanyStatus(StrEnum):
    HIDDEN = "hidden"
    VISIBLE = "visible"


class CompanyMemberRole(StrEnum):
    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELED = "canceled"
    REJECTED = "rejected"

class InvitationType(StrEnum):
    COMPANY_INVITE = "company_invite"
    USER_REQUEST = "user_request"