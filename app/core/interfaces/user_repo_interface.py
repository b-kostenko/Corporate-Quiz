from abc import ABC, abstractmethod
from typing import Dict, Tuple
from uuid import UUID

from pydantic import EmailStr

from app.infrastructure.postgres.models.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get(self, email: EmailStr) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> Tuple[list[User], int]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User, updates: Dict) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_password(self, user: User, new_password: str) -> None:
        raise NotImplementedError
