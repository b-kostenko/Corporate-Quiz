from pydantic import EmailStr

from app.core.repositories.user_repository import AbstractUserRepository
from app.core.schemas.user_schemas import TokenSchema, TokenType
from app.infrastructure.postgres.models.user import User
from app.infrastructure.security.jwt import create_token, decode_token, verify_token
from app.infrastructure.security.password import verify_password, hash_password
from app.settings import settings
from app.utils.exceptions import InvalidCredentials, ObjectNotFound


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository: AbstractUserRepository = user_repository

    async def get_current_user(self, token: str) -> User:
        verify = verify_token(token=token, token_type=TokenType.ACCESS)
        if not verify:
            raise InvalidCredentials("Invalid or expired access token")
        payload = decode_token(token=token)
        email = payload.get("sub")
        if not email:
            raise InvalidCredentials("Invalid token")
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound("User", email)
        return user

    async def login(self, email: EmailStr, password: str) -> TokenSchema:
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound(model_name="User", id_=email)

        if not verify_password(plain_password=password, hashed_password=user.password):
            raise InvalidCredentials("Invalid credentials provided")

        access_token = create_token(
            payload={"sub": user.email},
            token_type=TokenType.ACCESS,
            expire_minutes=settings.token.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh_token = create_token(
            payload={"sub": user.email},
            token_type=TokenType.REFRESH,
            expire_minutes=settings.token.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

        return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type=settings.token.TOKEN_TYPE)

    async def refresh_token(self, refresh_token: str) -> TokenSchema:
        verify = verify_token(token=refresh_token, token_type=TokenType.REFRESH)
        if not verify:
            raise InvalidCredentials("Invalid or expired refresh token")
        payload = decode_token(token=refresh_token)
        email = payload.get("sub")
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound("User", email)

        new_access_token = create_token(
            payload={"sub": user.email},
            token_type=TokenType.ACCESS,
            expire_minutes=settings.token.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return TokenSchema(
            access_token=new_access_token, refresh_token=refresh_token, token_type=settings.token.TOKEN_TYPE
        )

    async def change_password(self,email: EmailStr, old_password: str, new_password: str) -> None:
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound(model_name="User", id_=email)

        if not verify_password(plain_password=old_password, hashed_password=user.password):
            raise InvalidCredentials("Invalid credentials provided")

        hashed_new_password = hash_password(new_password)
        await self.user_repository.update_password(user=user, new_password=hashed_new_password)
