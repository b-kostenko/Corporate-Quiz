from uuid import UUID

from fastapi import APIRouter, Query
from starlette import status

from app.application.api.deps import current_user_deps, quiz_service_deps
from app.core.schemas import PaginatedResponse
from app.core.schemas.quiz_schemas import (
    AttemptQuizInputSchema,
    AttemptQuizOutputSchema,
    QuizAttemptRedisSchema,
    QuizInputSchema,
    QuizOutputSchema,
)

router = APIRouter(prefix="/quizzes", tags=["Quiz"])


@router.post("/{company_id}", response_model=QuizOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    company_id: UUID, quiz_payload: QuizInputSchema, quiz_service: quiz_service_deps, current_user: current_user_deps
) -> QuizOutputSchema:
    quiz = await quiz_service.create(company_id=company_id, user=current_user, quiz_payload=quiz_payload)
    return quiz


@router.put("/{quiz_id}/{company_id}", response_model=QuizOutputSchema, status_code=status.HTTP_200_OK)
async def update_quiz(
    quiz_id: UUID,
    company_id: UUID,
    quiz_payload: QuizInputSchema,
    quiz_service: quiz_service_deps,
    current_user: current_user_deps,
) -> QuizOutputSchema:
    quiz = await quiz_service.update(
        quiz_id=quiz_id, company_id=company_id, user=current_user, quiz_payload=quiz_payload
    )
    return quiz


@router.delete("/{quiz_id}/{company_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: UUID, company_id: UUID, quiz_service: quiz_service_deps, current_user: current_user_deps
) -> None:
    await quiz_service.delete(quiz_id=quiz_id, company_id=company_id, user=current_user)


@router.get("/{company_id}", response_model=PaginatedResponse[QuizOutputSchema], status_code=status.HTTP_200_OK)
async def get_company_quizzes(
    company_id: UUID,
    quiz_service: quiz_service_deps,
    current_user: current_user_deps,
    limit: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
) -> PaginatedResponse[QuizOutputSchema]:
    quizzes = await quiz_service.get_company_quizzes(
        company_id=company_id, user=current_user, limit=limit, offset=offset
    )
    return quizzes


@router.post("/{quiz_id}/{company_id}/attempts", response_model=AttemptQuizOutputSchema, status_code=status.HTTP_200_OK)
async def attempt_quiz(
    quiz_payload: AttemptQuizInputSchema,
    quiz_id: UUID,
    company_id: UUID,
    quiz_service: quiz_service_deps,
    current_user: current_user_deps,
) -> AttemptQuizOutputSchema:
    attempt = await quiz_service.attempt_quiz(
        quiz_payload=quiz_payload, quiz_id=quiz_id, company_id=company_id, user=current_user
    )
    return attempt

@router.get("/{quiz_id}/{company_id}/attempts", response_model=QuizAttemptRedisSchema, status_code=status.HTTP_200_OK, description="Get quiz attempts from Redis for 48 hours")
async def get_quiz_attempts(
    quiz_id: UUID,
    company_id: UUID,
    quiz_service: quiz_service_deps,
    current_user: current_user_deps
) -> QuizAttemptRedisSchema:
    attempts = await quiz_service.get_quiz_attempts(
        quiz_id=quiz_id, company_id=company_id, user=current_user
    )
    return attempts