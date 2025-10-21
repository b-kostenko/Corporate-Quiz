from urllib.parse import urlencode

from fastapi import APIRouter
from pydantic import EmailStr
from starlette import status
from starlette.responses import RedirectResponse

from app.application.api.deps import auth_service_deps, current_user_deps
from app.core.schemas.user_schemas import (
    RefreshTokenRequestSchema,
    ResetPasswordSchema,
    TokenSchema,
    UserLoginSchema,
    UserPasswordUpdateSchema,
)
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Login")
async def login(login_data: UserLoginSchema, auth_service: auth_service_deps):
    return await auth_service.login(email=login_data.email, password=login_data.password)


@router.post("/refresh", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Refresh token")
async def refresh_token(body: RefreshTokenRequestSchema, auth_service: auth_service_deps):
    return await auth_service.refresh_token(refresh_token=body.refresh_token)


@router.patch("/change-password", response_model=None, status_code=status.HTTP_204_NO_CONTENT, description="Change password")
async def change_password(payload: UserPasswordUpdateSchema, auth_service: auth_service_deps, current_user: current_user_deps):
    await auth_service.change_password(
        email=current_user.email, old_password=payload.old_password, new_password=payload.new_password
    )

@router.post("/reset-password", response_model=None, status_code=status.HTTP_200_OK, description="Reset password")
async def reset_password(email: EmailStr, auth_service: auth_service_deps = auth_service_deps):
    await auth_service.reset_password(email=email)


@router.post("/confirm-reset-password", response_model=None, status_code=status.HTTP_200_OK, description="Confirm reset password")
async def confirm_reset_password(payload: ResetPasswordSchema, token: str, uid: str, auth_service: auth_service_deps = auth_service_deps):
    await auth_service.confirm_reset_password(token=token, uid=uid, new_password=payload.new_password)


@router.get("/azure/login", status_code=status.HTTP_302_FOUND, description="Azure SSO login")
async def azure_login(auth_service: auth_service_deps):
    url = await auth_service.get_azure_login_url()
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)


@router.get("/azure/callback", status_code=status.HTTP_302_FOUND, description="Azure SSO callback")
async def azure_callback(code: str, auth_service: auth_service_deps):
    user = await auth_service.handle_azure_callback(code=code)
    tokens = auth_service.generate_tokens_for_user(user=user)
    redirect_url = f"{settings.FRONTEND_URL}/login/success?{urlencode(tokens.model_dump())}"
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)


@router.get("/google/login", status_code=status.HTTP_302_FOUND, description="Google SSO login")
async def google_login(auth_service: auth_service_deps):
    url = await auth_service.get_google_login_url()
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)


@router.get("/google/callback", status_code=status.HTTP_302_FOUND, description="Google SSO callback")
async def google_callback(code: str, auth_service: auth_service_deps):
    user = await auth_service.handle_google_callback(code=code)
    tokens = auth_service.generate_tokens_for_user(user=user)
    redirect_url = f"{settings.FRONTEND_URL}/login/success?{urlencode(tokens.model_dump())}"
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
