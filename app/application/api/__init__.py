from fastapi import APIRouter

from app.application.api import auth, users, companies

routers = APIRouter()

routers.include_router(users.router)
routers.include_router(auth.router)
routers.include_router(companies.router)
