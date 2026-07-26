from typing import List, Optional, Union

import redis.asyncio as aioredis

from .define import (
    ACCESS_TTL,
    REFRESH_TTL,
    access,
    access_idx,
    refresh,
    refresh_idx,
)
from .scripts import DEL_SESSION, NEW_SESSION, REFRESH_SESSION


class SessionStore:
    """Store and atomically mutate one active Redis session per user."""

    def __init__(self, redis: aioredis.Redis) -> None:
        self._redis = redis

    async def verify_access(self, token: str) -> Optional[str]:
        if not token:
            raise ValueError("token must not be empty")

        return await self._redis.get(name=access(token))  # type: ignore

    async def verify_refresh(self, token: str) -> Optional[str]:
        if not token:
            raise ValueError("token must not be empty")

        return await self._redis.get(name=refresh(token))  # type: ignore

    async def _run_script(
        self,
        script: str,
        keys: List[str],
        args: List[Union[str, int]],
    ) -> int:
        result = await self._redis.eval(script, len(keys), *keys, *args)
        if type(result) is not int:
            raise TypeError(
                f"Redis Lua script returned {type(result).__name__}, expected int"
            )
        return result

    async def create(
        self,
        uid: str,
        access_token: str,
        refresh_token: Optional[str] = None,
    ) -> bool:
        """Revoke the old session and create a new one."""
        if not uid:
            raise ValueError("uid must not be empty")
        if not access_token:
            raise ValueError("access_token must not be empty")
        if refresh_token == "":
            raise ValueError("refresh_token must not be empty")

        keys = [access_idx(uid), refresh_idx(uid), access(access_token)]
        args: List[Union[str, int]] = [uid, ACCESS_TTL]

        if refresh_token is not None:
            keys.append(refresh(refresh_token))
            args.append(REFRESH_TTL)

        return await self._run_script(NEW_SESSION, keys, args) == 1

    async def revoke(self, uid: str) -> int:
        """Revoke the current session and return the deleted key count."""
        if not uid:
            raise ValueError("uid must not be empty")

        return await self._run_script(
            DEL_SESSION,
            [access_idx(uid), refresh_idx(uid)],
            [],
        )

    async def refresh(
        self,
        uid: str,
        refresh_token: str,
        new_access_token: str,
    ) -> bool:
        """Validate the refresh token and atomically replace the access token."""
        if not uid:
            raise ValueError("uid must not be empty")
        if not refresh_token:
            raise ValueError("refresh_token must not be empty")
        if not new_access_token:
            raise ValueError("new_access_token must not be empty")

        return (
            await self._run_script(
                REFRESH_SESSION,
                [
                    access_idx(uid),
                    refresh_idx(uid),
                    refresh(refresh_token),
                    access(new_access_token),
                ],
                [uid, ACCESS_TTL],
            )
            == 1
        )


__all__ = ["SessionStore"]
