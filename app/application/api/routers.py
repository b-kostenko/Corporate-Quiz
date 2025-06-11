from fastapi import APIRouter

from app.application.api import users, auth

routers = APIRouter()

routers.include_router(users.router, prefix="/users", tags=["Users"])
routers.include_router(auth.router, prefix="/auth", tags=["Auth"])
