from typing import Optional

import redis.asyncio as aioredis

from ..common import RedisConfig


class RedisClient:
    """Own one lazily-created Redis client and its connection pool."""

    def __init__(self, config: Optional[RedisConfig] = None) -> None:
        self._config = config
        self._client: Optional[aioredis.Redis] = None

    def get(self) -> aioredis.Redis:
        if self._client is None:
            config = self._config or RedisConfig()
            pool = aioredis.ConnectionPool(
                host=config.host,
                port=config.port,
                username=config.user,
                password=config.password,
                db=0,
                max_connections=10,
                decode_responses=True,
            )
            self._client = aioredis.Redis(
                connection_pool=pool,
                protocol=2,
            )

        return self._client

    async def close(self) -> None:
        if self._client is None:
            return

        await self._client.aclose(close_connection_pool=True)
        self._client = None


__all__ = ["RedisClient"]
