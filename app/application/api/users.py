from typing import List

from fastapi import APIRouter
from starlette import status

from app.application.api.deps import current_user_deps, user_service_deps
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOutputSchema], status_code=status.HTTP_200_OK)
async def get_users(user_service: user_service_deps, _: current_user_deps):
    users = await user_service.get_all()
    return users


@router.get("/", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def get_user(user_service: user_service_deps, user: current_user_deps):
    user = await user_service.get(email=user.email)
    return user


@router.post("/", response_model=UserOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_input: UserInputSchema, user_service: user_service_deps):
    user = await user_service.create(user_input=user_input)
    return user


@router.put("/", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def update_user(user_input: UserUpdateSchema, user_service: user_service_deps, user: current_user_deps):
    user = await user_service.update(user=user, user_input=user_input)
    return user


@router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: current_user_deps, user_service: user_service_deps):
    await user_service.delete(user=user)
