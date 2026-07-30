from ..client import RedisClient
from .model import UserCache
from .define import user, USER_CACHE_TTL


async def set_user_cache(uid: str, cache: UserCache):
    await RedisClient.set(
        user(uid),
        cache.model_dump_json(),
        ex=USER_CACHE_TTL,
    )


async def delete_user_cache(uid: str):
    await RedisClient.delete(uid)
