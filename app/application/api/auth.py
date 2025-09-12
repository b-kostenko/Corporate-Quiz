from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import RedirectResponse

from app.application.api.deps import auth_service_deps, current_user_deps
from app.core.schemas.user_schemas import (
    RefreshTokenRequestSchema,
    TokenSchema,
    UserLoginSchema,
    UserPasswordUpdateSchema,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Login")
async def login_user(login_data: UserLoginSchema, auth_service: auth_service_deps):
    return await auth_service.login(email=login_data.email, password=login_data.password)


@router.post("/refresh", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Refresh token")
async def refresh_token(body: RefreshTokenRequestSchema, auth_service: auth_service_deps):
    return await auth_service.refresh_token(refresh_token=body.refresh_token)


@router.patch("/change-password", response_model=None, status_code=status.HTTP_204_NO_CONTENT, description="Change password")
async def change_password(payload: UserPasswordUpdateSchema, auth_service: auth_service_deps, current_user: current_user_deps):
    await auth_service.change_password(
        email=current_user.email, old_password=payload.old_password, new_password=payload.new_password
    )


@router.get("/azure/login", response_model=None, status_code=status.HTTP_200_OK, description="Azure SSO login")
async def login(auth_service: auth_service_deps):
    url = await auth_service.get_azure_login_url()
    return RedirectResponse(url)


@router.post("/azure/callback", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Azure SSO callback")
async def azure_callback(request: Request, auth_service: auth_service_deps):
    form = await request.form()
    user = await auth_service.handle_azure_callback(id_token=form.get("id_token"))
    tokens = auth_service.generate_tokens_for_user(user=user)
    return tokens