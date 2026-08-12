from ..client import RedisClient
from .define import Prefix, SESSION_CACHE_TTL
from .model import MessageCache


async def push_message(session_id: str, msg: MessageCache):
    key = Prefix.session(session_id)

    async with RedisClient.pipeline() as pipe:
        pipe.rpush(key, msg.model_dump_json())
        pipe.expire(key, SESSION_CACHE_TTL)


async def get_messages(session_id: str) -> list[MessageCache]:
    key = Prefix.session(session_id)

    async with RedisClient.pipeline(auto_execute=False) as pipe:
        pipe.lrange(key, 0, -1)
        pipe.expire(key, SESSION_CACHE_TTL)

    result = await pipe.execute()
    if not result:
        return []

    ans = result[0]

    return [MessageCache.model_validate_json(i) for i in ans] if ans else []
