from enum import StrEnum


class CompanyStatus(StrEnum):
    HIDDEN = "hidden"
    VISIBLE = "visible"


class CompanyMemberRole(StrEnum):
    MEMBER = "member"
    ADMIN = "admin"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELED = "canceled"