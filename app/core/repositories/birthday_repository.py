from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.birthday_repo_interface import AbstractBirthdayRepository
from app.infrastructure.postgres.models.birthday import Birthday
from app.infrastructure.postgres.models.user import User
from app.infrastructure.postgres.session_manager import provide_async_session


class BirthdayRepository(AbstractBirthdayRepository):
    @provide_async_session
    async def create(self, birthday: Birthday, session: AsyncSession) -> Birthday:
        session.add(birthday)
        await session.commit()
        await session.refresh(birthday)
        return birthday

    @provide_async_session
    async def get(self, user: User, birthday_person_name: str, session: AsyncSession) -> Birthday | None:
        query = select(Birthday).where((Birthday.owner_id == user.id) & (Birthday.person_name == birthday_person_name))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @provide_async_session
    async def get_all(self, user: User, session: AsyncSession) -> Sequence[Birthday]:
        query = select(Birthday).where(Birthday.owner_id == user.id)
        result = await session.execute(query)
        return result.scalars().all()

    @provide_async_session
    async def delete(self, user: User, birthday_person_name: str, session: AsyncSession) -> None:
        birthday = await self.get(user=user, birthday_person_name=birthday_person_name, session=session)
        await session.delete(birthday)
