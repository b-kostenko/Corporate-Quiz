from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, UUID4


class UserInputSchema(BaseModel):
    """Schema for user input data."""

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    birth_date: datetime | None = None
    avatar_url: str | None = None


class UserOutputSchema(BaseModel):
    """Schema for user output data."""

    id: UUID4
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    birth_date: datetime | None = None
    avatar_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True  # Enable ORM mode to work with SQLAlchemy models


class UserUpdateSchema(BaseModel):
    """Schema for updating user data."""
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    birth_date: datetime | None = None
    avatar_url: str | None = None


class UserPasswordUpdateSchema(BaseModel):
    """Schema for updating user password."""

    old_password: str
    new_password: str

    class Config:
        str_min_length = 1  # Ensure that passwords are not empty


class UserLoginSchema(BaseModel):
    """Schema for user login data."""

    email: str
    password: str

    class Config:
        str_min_length = 1  # Ensure that username and password are not empty


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
