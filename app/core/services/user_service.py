from abc import ABC, abstractmethod
from typing import List

from pydantic import EmailStr
from passlib.context import CryptContext

from app.core.repositories.user_repository import AbstractUserRepository
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema, TokenSchema
from app.infrastructure.postgres.models.user import User
from app.infrastructure.security.password import hash_password
from app.utils.exceptions import ObjectAlreadyExists, ObjectNotFound

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractUserService(ABC):

    @abstractmethod
    def create(self, user_input: UserInputSchema) -> UserOutputSchema:
        raise NotImplementedError

    @abstractmethod
    def get(self, email: EmailStr) -> UserOutputSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[UserOutputSchema]:
        raise NotImplementedError

    @abstractmethod
    def update(self, email: EmailStr, updates: UserInputSchema) -> UserOutputSchema:
        raise NotImplementedError

    @abstractmethod
    def delete(self, email: EmailStr) -> None:
        raise NotImplementedError


class UserService(AbstractUserService):

    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository: AbstractUserRepository = user_repository

    async def create(self, user_input: UserInputSchema) -> UserOutputSchema:
        user_exists = await self.user_repository.get(email=user_input.email)
        if user_exists:
            raise ObjectAlreadyExists(f"User with this email: {user_input.email} already exists.")

        user_input.password = hash_password(user_input.password)
        user = User(**user_input.model_dump())
        created_user = await self.user_repository.create(user=user)
        return UserOutputSchema.model_validate(created_user)

    async def get(self, email: EmailStr) -> UserOutputSchema | None:
        response = await self.user_repository.get(email=email)
        if not response:
            return None
        return UserOutputSchema.model_validate(response)

    async def get_all(self) -> list[UserOutputSchema]:
        users = await self.user_repository.get_all()
        return [UserOutputSchema.model_validate(user) for user in users]

    async def update(self, user: User, user_input: UserInputSchema) -> UserOutputSchema:
        response = await self.user_repository.update(user=user, updates=user_input.model_dump())
        return UserOutputSchema.model_validate(response)

    async def delete(self, user: User) -> None:
        await self.user_repository.delete(user=user)
