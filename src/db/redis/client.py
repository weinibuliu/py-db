from typing import Any, Optional

import redis.asyncio as aioredis

from ..common import RedisConfig


class RedisClient:
    """Own the process-wide lazy Redis client and its connection pool."""

    _client: Optional[aioredis.Redis] = None

    @classmethod
    def create_client(cls) -> None:
        if cls._client is None:
            config = RedisConfig()
            pool = aioredis.ConnectionPool(
                host=config.host,
                port=config.port,
                username=config.user,
                password=config.password,
                db=0,
                max_connections=10,
                decode_responses=True,
            )
            cls._client = aioredis.Redis(
                connection_pool=pool,
                protocol=2,
            )

    @classmethod
    def get_client(cls) -> aioredis.Redis:
        if cls._client is None:
            cls.create_client()

        assert cls._client is not None
        return cls._client

    @classmethod
    async def close_client(cls) -> None:
        if cls._client is None:
            return

        await cls._client.aclose(close_connection_pool=True)
        cls._client = None

    @classmethod
    async def get(cls, name: str) -> Optional[str]:
        return await cls.get_client().get(name)  # type: ignore

    @classmethod
    async def set(cls, name: str, value: str, ex: int = -1) -> None:
        await cls.get_client().set(name, value, ex=ex)

    @classmethod
    async def delete(cls, *keys: str):
        await cls.get_client().delete(*keys)

    @classmethod
    async def eval(cls, script: str, numkeys: int, *keys_and_args: Any) -> int:
        return await cls.get_client().eval(script, numkeys, *keys_and_args)

    @classmethod
    async def incr(cls, name: str, amount: int = 1) -> int:
        """key += amount"""
        return await cls.get_client().incr(name, amount)

    @classmethod
    async def decr(cls, name: str, amount: int = 1) -> int:
        """key -= amount"""
        return await cls.get_client().decr(name, amount)


create_redis = RedisClient.create_client
close_redis = RedisClient.close_client


__all__ = [
    "create_redis",
    "close_redis",
]
