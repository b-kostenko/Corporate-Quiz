from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

engine = create_async_engine(settings.database.DATABASE_URL, echo=False, poolclass=NullPool)

DeclarativeBase = declarative_base()

AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
