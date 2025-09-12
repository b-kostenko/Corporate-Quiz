import redis.asyncio as redis
from pydantic import EmailStr


class AsyncRedisRepository:
    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    async def set(self, key: str | EmailStr, value: str, ex: int = None) -> None:
        await self.client.set(name=key, value=value, ex=ex)

    async def get(self, key: str) -> str | None:
        return await self.client.get(name=key)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) == 1
