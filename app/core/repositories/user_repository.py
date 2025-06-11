from abc import ABC, abstractmethod
from typing import Dict, Sequence

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models.user import User
from app.infrastructure.postgres.session_manager import provide_async_session


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get(self, email: EmailStr) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User, updates: Dict, ) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError


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
