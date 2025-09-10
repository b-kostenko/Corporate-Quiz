from fastapi import APIRouter

from app.application.api import auth, users, companies, company_actions

routers = APIRouter()

routers.include_router(users.router)
routers.include_router(auth.router)
routers.include_router(companies.router)
routers.include_router(company_actions.router)
