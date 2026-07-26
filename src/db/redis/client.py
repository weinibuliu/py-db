from typing import Optional

import redis.asyncio as aioredis

from ..common import RedisConfig


class RedisClient:
    """Own the process-wide lazy Redis client and its connection pool."""

    _client: Optional[aioredis.Redis] = None

    @classmethod
    def create(cls) -> None:
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
    def get(cls) -> aioredis.Redis:
        if cls._client is None:
            cls.create()

        assert cls._client is not None
        return cls._client

    @classmethod
    async def close(cls) -> None:
        if cls._client is None:
            return

        await cls._client.aclose(close_connection_pool=True)
        cls._client = None


create_redis = RedisClient.create
close_redis = RedisClient.close


__all__ = ["create_redis", "close_redis"]
