from typing import List

from fastapi import APIRouter
from pydantic import UUID4

from app.application.api.deps import current_user_deps, birthday_service_deps
from app.core.schemas.birthdays_schemas import BirthdayInputSchema, BirthdayOutputSchema

router = APIRouter(prefix="/birthdays", tags=["Birthdays"])



@router.post("/",response_model=BirthdayOutputSchema, status_code=201, description="Create Birthday")
async def create_birthday(user_input: BirthdayInputSchema, user: current_user_deps, birthday_service: birthday_service_deps):
    birthday = await birthday_service.create(user=user, user_input=user_input)
    return birthday


@router.get("/",response_model=List[BirthdayOutputSchema], status_code=200, description="Get Birthdays")
async def get_birthdays(user: current_user_deps, birthday_service: birthday_service_deps):
    birthdays = await birthday_service.get_all(user=user)
    return birthdays

@router.delete("/{birthday_person_name}", status_code=204, description="Delete Birthday")
async def delete_birthday(birthday_person_name: str, user: current_user_deps, birthday_service: birthday_service_deps):
    await birthday_service.delete(user=user, birthday_person_name=birthday_person_name)
    return None


