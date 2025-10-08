from typing import Dict, Tuple
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import func, select
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
    async def get_by_id(self, user_id: UUID, session: AsyncSession) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @provide_async_session
    async def get_all(self, limit: int, offset: int, session: AsyncSession) -> Tuple[list[User], int]:
        count_query = select(func.count(User.id))
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        query = select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        result = await session.execute(query)
        users = result.scalars().all()
        return list(users), total


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

    @provide_async_session
    async def update_password(self, user: User, new_password: str, session: AsyncSession) -> None:
        user = await session.merge(user)
        user.password = new_password
        await session.commit()
