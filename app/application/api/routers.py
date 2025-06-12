from fastapi import APIRouter

from app.application.api import auth, birthdays, users

routers = APIRouter()

routers.include_router(users.router, prefix="/users", tags=["Users"])
routers.include_router(auth.router, prefix="/auth", tags=["Auth"])
routers.include_router(birthdays.router, prefix="/birthdays", tags=["Birthdays"])
