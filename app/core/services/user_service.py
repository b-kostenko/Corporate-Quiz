from uuid import UUID

from pydantic import EmailStr

from app.core.interfaces.user_serv_interface import AbstractUserService
from app.core.repositories.user_repository import AbstractUserRepository
from app.core.schemas import PaginatedResponse, PaginationMeta
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema
from app.infrastructure.postgres.models.user import User
from app.infrastructure.security.password import hash_password
from app.utils.exceptions import ObjectAlreadyExists, ObjectNotFound


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
            raise ObjectNotFound(model_name="User", id_=email)
        return UserOutputSchema.model_validate(response)

    async def get_by_id(self, uuid: UUID) -> UserOutputSchema | None:
        response = await self.user_repository.get_by_id(user_id=uuid)
        if not response:
            raise ObjectNotFound(model_name="User", id_=uuid)
        return UserOutputSchema.model_validate(response)

    async def get_all(self, limit: int, offset: int) -> PaginatedResponse[UserOutputSchema]:
        users, total  = await self.user_repository.get_all(limit=limit, offset=offset)

        user_schemas = [UserOutputSchema.model_validate(user) for user in users]
        meta = PaginationMeta(
            total=total, limit=limit, offset=offset, has_next=offset + limit < total, has_previous=offset > 0
        )

        return PaginatedResponse[UserOutputSchema](items=user_schemas, meta=meta)

    async def update(self, user: User, user_input: UserInputSchema) -> UserOutputSchema:
        response = await self.user_repository.update(user=user, updates=user_input.model_dump())
        return UserOutputSchema.model_validate(response)

    async def delete(self, user: User) -> None:
        await self.user_repository.delete(user=user)

    async def update_avatar(self, user_avatar: str, user: User) -> UserOutputSchema:
        response = await self.user_repository.get(email=user.email)
        if not response:
            raise ObjectNotFound(model_name="User", id_=user.email)

        response = await self.user_repository.update(user=user, updates={"avatar_url": user_avatar})
        return UserOutputSchema.model_validate(response)
