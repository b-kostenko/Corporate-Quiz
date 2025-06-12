import contextlib
from functools import wraps
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.connection import AsyncSessionLocal


@contextlib.asynccontextmanager
async def create_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async contextmanager that will create and teardown a session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def provide_async_session(func):
    """
    Function decorator that provides an async session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        arg_session = "session"

        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs

        if session_in_kwargs or session_in_args:
            return await func(*args, **kwargs)
        else:
            async with create_async_session() as session:
                kwargs[arg_session] = session
                return await func(*args, **kwargs)

    return wrapper
