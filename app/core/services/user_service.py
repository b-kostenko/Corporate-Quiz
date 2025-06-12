from typing import List

from pydantic import EmailStr

from app.core.interfaces.user_serv_interface import AbstractUserService
from app.core.repositories.user_repository import AbstractUserRepository
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema
from app.infrastructure.postgres.models.user import User
from app.infrastructure.security.password import hash_password
from app.utils.exceptions import ObjectAlreadyExists


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

    async def get_all(self) -> List[UserOutputSchema]:
        users = await self.user_repository.get_all()
        return [UserOutputSchema.model_validate(user) for user in users]

    async def update(self, user: User, user_input: UserInputSchema) -> UserOutputSchema:
        response = await self.user_repository.update(user=user, updates=user_input.model_dump())
        return UserOutputSchema.model_validate(response)

    async def delete(self, user: User) -> None:
        await self.user_repository.delete(user=user)
