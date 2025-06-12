from typing import Dict, Sequence

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.user_repo_interface import AbstractUserRepository
from app.infrastructure.postgres.models.user import User
from app.infrastructure.postgres.session_manager import provide_async_session


class UserRepository(AbstractUserRepository):
    @provide_async_session
    async def create(self, user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @provide_async_session
    async def get(self, email: EmailStr, session: AsyncSession) -> User | None:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @provide_async_session
    async def get_all(self, session: AsyncSession) -> Sequence[User]:
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()

    @provide_async_session
    async def update(self, user: User, updates: Dict, session: AsyncSession) -> User:
        user = await session.merge(user)
        for key, value in updates.items():
            if value is not None:
                setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user

    @provide_async_session
    async def delete(self, user: User, session: AsyncSession) -> None:
        await session.delete(user)
        await session.commit()
