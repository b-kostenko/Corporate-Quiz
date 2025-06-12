from abc import ABC, abstractmethod
from typing import List

from app.core.schemas.birthdays_schemas import BirthdayInputSchema, BirthdayOutputSchema
from app.infrastructure.postgres.models.user import User


class AbstractBirthdayService(ABC):
    @abstractmethod
    def create(self, user: User, user_input: BirthdayInputSchema) -> BirthdayOutputSchema:
        raise NotImplementedError

    @abstractmethod
    def get(self, user: User, birthday_person_name: str) -> BirthdayOutputSchema:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user: User) -> List[BirthdayOutputSchema]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: User, birthday_person_name: str) -> None:
        raise NotImplementedError
