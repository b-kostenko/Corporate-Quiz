import secrets

from pydantic import EmailStr

from app.core.repositories.user_repository import AbstractUserRepository
from app.core.schemas.auth_schemas import AzureAuthorizationResponse
from app.core.schemas.user_schemas import TokenSchema, TokenType, UserInputSchema
from app.infrastructure.postgres.models.user import User
from app.infrastructure.security.jwt import create_token, decode_token, verify_token
from app.infrastructure.security.password import hash_password, verify_password
from app.settings import settings
from app.utils.exceptions import InvalidCredentials, ObjectNotFound


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository: AbstractUserRepository = user_repository

    async def get_current_user(self, token: str) -> User:
        verify = verify_token(token=token, token_type=TokenType.ACCESS)
        if not verify:
            raise InvalidCredentials("Invalid or expired access token")
        payload = decode_token(token=token, key=settings.token.SECRET_KEY, algorithms=[settings.token.ALGORITHM], options={})
        email = payload.get("sub")
        if not email:
            raise InvalidCredentials("Invalid token")
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound("User", email)
        return user

    def generate_tokens_for_user(self, user: User) -> TokenSchema:
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

    async def login(self, email: EmailStr, password: str) -> TokenSchema:
        user = await self.user_repository.get(email)
        if not user:
            raise ObjectNotFound(model_name="User", id_=email)

        if not verify_password(plain_password=password, hashed_password=user.password):
            raise InvalidCredentials("Invalid credentials provided")

        return self.generate_tokens_for_user(user=user)

    async def refresh_token(self, refresh_token: str) -> TokenSchema:
        verify = verify_token(token=refresh_token, token_type=TokenType.REFRESH)
        if not verify:
            raise InvalidCredentials("Invalid or expired refresh token")
        payload = decode_token(token=refresh_token, key=settings.token.SECRET_KEY, algorithms=[settings.token.ALGORITHM], options={})
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

    async def get_azure_login_url(self, state: str | None = None, nonce: str | None = None) -> str:
        """Generate Azure AD OAuth2 authorization URL"""
        # Generate a secure random state parameter
        state = state or AzureAuthorizationResponse.generate_state()
        nonce = nonce or AzureAuthorizationResponse.generate_nonce()

        response = AzureAuthorizationResponse(
            authorization_endpoint=settings.azure_sso.AZURE_AUTHORITY,
            client_id=settings.azure_sso.AZURE_CLIENT_ID,
            redirect_uri=settings.azure_sso.AZURE_REDIRECT_URI,
            scope=" ".join(settings.azure_sso.AZURE_SCOPES),
            nonce=nonce,
            state=state
        )

        return response.generate_url()

    async def handle_azure_callback(self, id_token: str) -> User:
        token_payload = decode_token(
            token=id_token,
            key=settings.token.SECRET_KEY,
            algorithms=None,
            options={"verify_signature": False}
        )

        user_input = UserInputSchema(
            first_name=token_payload.get("given_name"),
            last_name=token_payload.get("family_name"),
            email=token_payload.get("email"),
            password=hash_password(secrets.token_urlsafe(16))
        )

        existing_user = await self.user_repository.get(email=user_input.email)
        if existing_user:
            return existing_user

        new_user = User(**user_input.model_dump())
        created_user = await self.user_repository.create(user=new_user)
        return created_user
