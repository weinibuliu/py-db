import asyncio
from typing import Optional

import redis.asyncio as aioredis

from .define import (
    ACCESS_TTL,
    REFRESH_TTL,
    access,
    access_idx,
    refresh,
    refresh_idx,
)
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
    async def set_access_token(cls, token: str, uid: str):
        """
        NOTE: 在 /login 接口内调用时 应当先执行 `clear_tokens` 吊销已有 tokens
        """
        access_token = access(token)
        access_index = access_idx(uid)

        r = cls.get_redis()
        async with r.pipeline(transaction=True) as pipe:
            # ACC:{token} -> uid
            # u_acc:{uid} -> ACC:{token}
            pipe.set(name=access_token, value=uid, ex=ACCESS_TTL)
            pipe.set(name=access_index, value=access_token, ex=ACCESS_TTL)
            await pipe.execute()

    @classmethod
    async def set_refresh_token(cls, token: str, uid: str):
        refresh_token = refresh(token)
        refresh_index = refresh_idx(uid)

        r = cls.get_redis()
        async with r.pipeline(transaction=True) as pipe:
            # REF:{token} -> uid
            # u_ref:{uid} -> REF:{token}
            pipe.set(name=refresh_token, value=uid, ex=REFRESH_TTL)
            pipe.set(name=refresh_index, value=refresh_token, ex=REFRESH_TTL)
            await pipe.execute()

    @classmethod
    async def set_tokens(cls, access_token: str, refresh_token: str, uid: str):
        access_token = access(access_token)
        access_index = access_idx(uid)
        refresh_token = refresh(refresh_token)
        refresh_index = refresh_idx(uid)

        r = cls.get_redis()
        async with r.pipeline(transaction=True) as pipe:
            pipe.set(name=access_token, value=uid, ex=ACCESS_TTL)
            pipe.set(name=access_index, value=access_token, ex=ACCESS_TTL)
            pipe.set(name=refresh_token, value=uid, ex=REFRESH_TTL)
            pipe.set(name=refresh_index, value=refresh_token, ex=REFRESH_TTL)
            await pipe.execute()

    @classmethod
    async def clear_access_token(cls, uid: str):
        r = cls.get_redis()

        idx = access_idx(uid)
        token = await r.get(idx)
        if token is None or type(token) != str:
            return

        async with r.pipeline(transaction=True) as pipe:
            pipe.delete(idx)
            pipe.delete(token)
            await pipe.execute()

    # NOTE: 不单独提供吊销 refresh_token 的吊销方法 即清除 refresh 时一并清除 access
    # @classmethod
    # async def clear_refresh_token(cls, uid: str):
    #     r = cls.get_redis()

    #     idx = refresh_idx(uid)
    #     token = await r.get(idx)
    #     if token is None or type(token) != str:
    #         return

    #     async with r.pipeline(transaction=True) as pipe:
    #         pipe.delete(idx)
    #         pipe.delete(token)
    #         await pipe.execute()

    @classmethod
    async def clear_tokens(cls, uid: str):
        r = cls.get_redis()

        acc_idx = access_idx(uid)
        ref_idx = refresh_idx(uid)
        acc_token, ref_token = await asyncio.gather(r.get(acc_idx), r.get(ref_idx))

        async with r.pipeline(transaction=True) as pipe:
            if isinstance(acc_token, str):
                pipe.delete(acc_token)
                pipe.delete(acc_idx)
            if isinstance(ref_token, str):
                pipe.delete(ref_token)
                pipe.delete(ref_idx)
            await pipe.execute()
