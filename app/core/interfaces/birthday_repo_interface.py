from abc import ABC, abstractmethod
from typing import Sequence

from app.infrastructure.postgres.models.birthday import Birthday
from app.infrastructure.postgres.models.user import User


class AbstractBirthdayRepository(ABC):
    @abstractmethod
    async def create(self, birthday: Birthday) -> Birthday:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user: User, birthday_person_name: str) -> Birthday | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, user: User) -> Sequence[Birthday]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User, birthday_person_name: str) -> None:
        raise NotImplementedError
