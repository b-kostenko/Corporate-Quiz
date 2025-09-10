from fastapi import APIRouter
from uuid import UUID

from app.application.api.deps import current_user_deps, quiz_service_deps
from app.core.schemas.quiz_schemas import QuizInputSchema, QuizOutputSchema

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/{company_id}", response_model=QuizOutputSchema, status_code=201)
async def create_quiz(quiz_payload: QuizInputSchema, company_id: UUID, quiz_service: quiz_service_deps, current_user: current_user_deps):
    quiz = await quiz_service.create(company_id=company_id, user=current_user, quiz_payload=quiz_payload)
    return quiz


