from fastapi import APIRouter

from app.application.api import auth, users, companies, company_actions, quiz

routers = APIRouter()

routers.include_router(users.router)
routers.include_router(auth.router)
routers.include_router(companies.router)
routers.include_router(company_actions.router)
routers.include_router(quiz.router)
