from typing import List

from app.core.interfaces.birthday_repo_interface import AbstractBirthdayRepository
from app.core.interfaces.birthday_serv_interface import AbstractBirthdayService
from app.core.schemas.birthdays_schemas import BirthdayInputSchema, BirthdayOutputSchema
from app.infrastructure.postgres.models.birthday import Birthday
from app.infrastructure.postgres.models.user import User
from app.utils.exceptions import ObjectNotFound, ObjectAlreadyExists


class BirthdayService(AbstractBirthdayService):

    def __init__(self, birthday_repository: AbstractBirthdayRepository):
        self.birthday_repository: AbstractBirthdayRepository = birthday_repository

    async def create(self, user: User, user_input: BirthdayInputSchema) -> BirthdayOutputSchema:
        birthday_person = await self.birthday_repository.get(user=user, birthday_person_name=user_input.person_name)
        if birthday_person:
            raise ObjectAlreadyExists(f"Birthday for {user_input.person_name} already exists.")

        birthday_payload = Birthday(**user_input.model_dump())
        birthday_payload.owner_id = user.id
        created_birthday = await self.birthday_repository.create(birthday=birthday_payload)
        return BirthdayOutputSchema.model_validate(created_birthday)

    async def get(self, user: User, birthday_person_name: str) -> BirthdayOutputSchema | None:
        birthday = await self.birthday_repository.get(user=user, birthday_person_name=birthday_person_name)
        if not birthday:
            raise ObjectNotFound(model_name="Birthday", id_=birthday_person_name)
        return BirthdayOutputSchema.model_validate(birthday)

    async def get_all(self, user: User) -> List[BirthdayOutputSchema]:
        birthdays = await self.birthday_repository.get_all(user=user)
        return [BirthdayOutputSchema.model_validate(birthday) for birthday in birthdays]

    async def delete(self, user: User, birthday_person_name: str) -> None:
        await self.birthday_repository.delete(user=user, birthday_person_name=birthday_person_name)
