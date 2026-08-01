from ..client import RedisClient
from .model import UserCache
from .define import Prefix, USER_CACHE_TTL
from ..._db.crud.read import get_user_by_uid
from ...common import NotFoundError


async def set_user_cache(uid: str, cache: UserCache):
    await RedisClient.set(
        Prefix.user(uid),
        cache.model_dump_json(),
        ex=USER_CACHE_TTL,
    )


async def revoke_user_cache(uid: str):
    await RedisClient.delete(Prefix.user(uid))


async def read_user_cache(uid: str) -> UserCache:
    """如果查表和缓存均失败 抛出 NotFoundError"""

    r = await RedisClient.get(Prefix.user(uid))
    if r is not None:
        return UserCache.model_validate_json(r)

    usr = get_user_by_uid(uid)
    if usr is None:
        raise NotFoundError()
    else:
        return UserCache(**usr.model_dump())


async def set_user_caches(uid_list: list[str], cache_list: list[UserCache]):
    async with RedisClient.pipeline(transaction=False) as pipe:
        for uid, cache in zip(uid_list, cache_list):
            pipe.set(
                Prefix.user(uid),
                cache.model_dump_json(),
                ex=USER_CACHE_TTL,
            )


async def revoke_user_caches(uid_list: list[str]):
    async with RedisClient.pipeline(transaction=False) as pipe:
        for uid in uid_list:
            pipe.delete(Prefix.user(uid))
