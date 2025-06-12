from abc import ABC, abstractmethod
from typing import Dict, Sequence

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
    async def get_all(self, ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User, updates: Dict) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError

