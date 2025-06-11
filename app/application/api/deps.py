from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.repositories.user_repository import UserRepository
from app.core.services.auth_service import AuthService
from app.core.services.user_service import UserService

http_bearer = HTTPBearer()

def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository)


user_service_deps = Annotated[UserService, Depends(get_user_service)]
auth_service_deps = Annotated[AuthService, Depends(get_auth_service)]
token_deps = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]


async def get_current_user(auth_service: auth_service_deps, token: token_deps):
    return await auth_service.get_current_user(token.credentials)

current_user_deps = Annotated['User', Depends(get_current_user)]