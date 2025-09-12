from typing import List

from fastapi import APIRouter, UploadFile
from pydantic import EmailStr
from starlette import status

from app.application.api.deps import current_user_deps, file_storage_deps, user_service_deps
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOutputSchema], status_code=status.HTTP_200_OK)
async def get_users(user_service: user_service_deps, _: current_user_deps):
    users = await user_service.get_all()
    return users


@router.get("/profile", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def read_users_me(user_service: user_service_deps, current_user: current_user_deps):
    return await user_service.get(email=current_user.email)



@router.get("/{email}", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def get_user_by_email(email: EmailStr, user_service: user_service_deps):
    user = await user_service.get(email=email)
    return user


@router.post("/", response_model=UserOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_input: UserInputSchema, user_service: user_service_deps):
    user = await user_service.create(user_input=user_input)
    return user


@router.put("/", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def update_user(user_input: UserUpdateSchema, user_service: user_service_deps, user: current_user_deps):
    user = await user_service.update(user=user, user_input=user_input)
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(current_user: current_user_deps, user_service: user_service_deps):
    await user_service.delete(user=current_user)


@router.post("/avatar", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def update_avatar(avatar_file: UploadFile, user_service: user_service_deps, current_user: current_user_deps, file_storage: file_storage_deps):
    content = await avatar_file.read()
    user_avatar = await file_storage.save_file(content=content, filename=avatar_file.filename)
    user = await user_service.update_avatar(user_avatar=user_avatar, user=current_user)
    return user