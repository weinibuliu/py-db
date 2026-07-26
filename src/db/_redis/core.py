from typing import List, Optional, Union, overload

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
from ..common import RedisConfig


class RedisManager:
    r: Optional[aioredis.Redis] = None

    @classmethod
    def create_redis(cls) -> None:
        if cls.r is None:
            _cfg = RedisConfig()
            pool = aioredis.ConnectionPool(
                host=_cfg.host,
                port=_cfg.port,
                username=_cfg.user,
                password=_cfg.password,
                db=0,
                max_connections=10,
                decode_responses=True,
            )
            cls.r = aioredis.Redis(
                connection_pool=pool,
                protocol=2,
            )

    @classmethod
    async def close_redis(cls) -> None:
        if cls.r is None:
            return

        await cls.r.aclose(close_connection_pool=True)
        cls.r = None

    @classmethod
    def get_redis(cls) -> aioredis.Redis:
        if cls.r is None:
            cls.create_redis()

        assert cls.r is not None

        return cls.r

    @classmethod
    async def verify_access_token(cls, token: str) -> Optional[str]:
        return await cls.get_redis().get(name=access(token))  # type: ignore

    @classmethod
    async def verify_refresh_token(cls, token: str) -> Optional[str]:
        return await cls.get_redis().get(name=refresh(token))  # type: ignore

    @classmethod
    async def _run_script(
        cls,
        script: str,
        keys: List[str],
        args: List[Union[str, int]],
    ) -> int:
        result = await cls.get_redis().eval(script, len(keys), *keys, *args)
        if type(result) is not int:
            raise TypeError(
                f"Redis Lua script returned {type(result).__name__}, expected int"
            )
        return result

    @classmethod
    async def new_session(
        cls,
        uid: str,
        access_token: str,
        refresh_token: Optional[str] = None,
    ) -> bool:
        """撤销旧会话并创建新会话；refresh token 可选。"""
        assert uid
        assert access_token
        assert refresh_token != ""

        keys = [access_idx(uid), refresh_idx(uid), access(access_token)]
        args: List[Union[str, int]] = [uid, ACCESS_TTL]

        if refresh_token is not None:
            keys.append(refresh(refresh_token))
            args.append(REFRESH_TTL)

        return await cls._run_script(NEW_SESSION, keys, args) == 1

    @classmethod
    async def del_session(cls, uid: str) -> int:
        """撤销用户当前会话，返回实际删除的 Redis key 数量。"""
        if not uid:
            raise ValueError("uid must not be empty")

        return await cls._run_script(
            DEL_SESSION,
            [access_idx(uid), refresh_idx(uid)],
            [],
        )

    @classmethod
    async def refresh_session(
        cls,
        uid: str,
        refresh_token: str,
        new_access_token: str,
    ) -> bool:
        """校验当前 refresh token，并原子替换 access token。"""
        if not uid:
            raise ValueError("uid must not be empty")
        if not refresh_token:
            raise ValueError("refresh_token must not be empty")
        if not new_access_token:
            raise ValueError("new_access_token must not be empty")

        assert uid
        assert refresh_token
        assert new_access_token

        return (
            await cls._run_script(
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
