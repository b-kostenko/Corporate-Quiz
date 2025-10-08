from uuid import UUID

from fastapi import APIRouter, Query, UploadFile
from starlette import status

from app.application.api.deps import current_user_deps, file_storage_deps, user_service_deps
from app.core.schemas import PaginatedResponse
from app.core.schemas.user_schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginatedResponse[UserOutputSchema], status_code=status.HTTP_200_OK)
async def get_users(
        limit: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
        offset: int = Query(default=0, ge=0, description="Number of items to skip"),
        user_service: user_service_deps = None,
        _: current_user_deps = None,
):
    users = await user_service.get_all(limit=limit, offset=offset)
    return users


@router.get("/profile", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def read_users_me(user_service: user_service_deps, current_user: current_user_deps):
    return await user_service.get(email=current_user.email)



@router.get("/{uuid}", response_model=UserOutputSchema, status_code=status.HTTP_200_OK)
async def get_user_by_uuid(uuid: UUID, user_service: user_service_deps):
    user = await user_service.get_by_id(uuid=uuid)
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