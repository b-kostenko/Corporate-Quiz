from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.interfaces.file_storage_interface import FileStorageInterface
from app.core.repositories.company_repository import CompanyRepository
from app.core.repositories.quiz_repository import QuizRepository
from app.core.repositories.redis_repository import AsyncRedisRepository
from app.core.repositories.user_repository import UserRepository
from app.core.services.auth_service import AuthService
from app.core.services.company_service import CompanyService
from app.core.services.notification_service import AsyncEmailSender
from app.core.services.quiz_service import QuizService
from app.core.services.user_service import UserService
from app.infrastructure.postgres.models import User
from app.infrastructure.storage import create_local_storage
from app.settings import settings

http_bearer = HTTPBearer()


def get_email_sender() -> AsyncEmailSender:
    return AsyncEmailSender(
        host=settings.smtp.SMTP_EMAIL_HOST,
        port=settings.smtp.SMTP_EMAIL_PORT,
        username=settings.smtp.SMTP_EMAIL_USERNAME,
        password=settings.smtp.SMTP_EMAIL_PASSWORD,
        templates_dir=settings.TEMPLATES_DIR
    )


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        email_sender: AsyncEmailSender = Depends(get_email_sender)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        email_sender=email_sender
    )


user_service_deps = Annotated[UserService, Depends(get_user_service)]
auth_service_deps = Annotated[AuthService, Depends(get_auth_service)]
token_deps = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]


async def get_current_user(auth_service: auth_service_deps, token: token_deps):
    return await auth_service.get_current_user(token.credentials)


async def get_company_repository() -> CompanyRepository:
    return CompanyRepository()


async def get_company_service(company_repository=Depends(get_company_repository)):
    return CompanyService(company_repository=company_repository)


def get_file_storage() -> FileStorageInterface:
    """Get file storage instance."""
    return create_local_storage(settings.file_storage)


def get_quiz_repository() -> QuizRepository:
    return QuizRepository()

def get_redis_repository() -> AsyncRedisRepository:
    return AsyncRedisRepository(
        host=settings.redis.REDIS_HOST,
        port=settings.redis.REDIS_PORT,
        db=settings.redis.REDIS_DB_QUIZ_ANSWERS,
        password=settings.redis.REDIS_PASSWORD
    )

def get_quiz_service(
    company_repository: CompanyRepository = Depends(get_company_repository),
    quiz_repository: QuizRepository = Depends(get_quiz_repository),
    redis_repository: AsyncRedisRepository = Depends(get_redis_repository),
) -> QuizService:
    return QuizService(
        company_repository=company_repository,
        quiz_repository=quiz_repository,
        redis_repository=redis_repository
    )



current_user_deps = Annotated[User, Depends(get_current_user)]
company_service_deps = Annotated[CompanyService, Depends(get_company_service)]
file_storage_deps = Annotated[FileStorageInterface, Depends(get_file_storage)]
quiz_service_deps = Annotated[QuizService, Depends(get_quiz_service)]
