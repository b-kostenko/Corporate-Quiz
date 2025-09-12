from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserInputSchema(BaseModel):
    """Schema for user input data."""

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str


class UserOutputSchema(BaseModel):
    """Schema for user output data."""

    id: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    """Schema for updating user data."""

    first_name: str | None = None
    last_name: str | None = None


class UserPasswordUpdateSchema(BaseModel):
    """Schema for updating user password."""

    old_password: str
    new_password: str

    class Config:
        str_min_length = 1  # Ensure that passwords are not empty


class UserLoginSchema(BaseModel):
    """Schema for user login data."""

    email: EmailStr
    password: str

    class Config:
        str_min_length = 1


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str