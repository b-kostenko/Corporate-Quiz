from fastapi import APIRouter

from app.application.api import auth, companies, company_actions, quiz, users, user_actions

routers = APIRouter()

routers.include_router(users.router)
routers.include_router(auth.router)
routers.include_router(companies.router)
routers.include_router(user_actions.router)
routers.include_router(company_actions.router)
routers.include_router(quiz.router)
