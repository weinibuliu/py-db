from ..client import RedisClient
from .model import UserCache
from .define import _user, USER_CACHE_TTL
from ..._db.crud.read import get_user_by_uid
from ...common import NotFoundError


async def set_user_cache(uid: str, cache: UserCache):
    await RedisClient.set(
        _user(uid),
        cache.model_dump_json(),
        ex=USER_CACHE_TTL,
    )


async def revoke_user_cache(uid: str):
    await RedisClient.delete(_user(uid))


async def read_user_cache(uid: str) -> UserCache:
    r = await RedisClient.get(_user(uid))
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
                _user(uid),
                cache.model_dump_json(),
                ex=USER_CACHE_TTL,
            )


async def revoke_user_caches(uid_list: list[str]):
    async with RedisClient.pipeline(transaction=False) as pipe:
        for uid in uid_list:
            pipe.delete(_user(uid))
