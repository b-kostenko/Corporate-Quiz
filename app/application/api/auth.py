from fastapi import APIRouter
from starlette import status

from app.application.api.deps import auth_service_deps
from app.core.schemas.user_schemas import TokenSchema, UserLoginSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Login")
async def login_user(login_data: UserLoginSchema, auth_service: auth_service_deps):
    return await auth_service.login(email=login_data.email, password=login_data.password)

@router.get("/refresh", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Refresh token")
async def refresh_token(token: str, auth_service: auth_service_deps):
    return await auth_service.refresh_token(refresh_token=token)

