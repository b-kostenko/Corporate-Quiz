from abc import ABC, abstractmethod
from typing import List

from pydantic import EmailStr

from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema


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
