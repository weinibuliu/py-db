from asyncio import to_thread
from typing import Optional

from .define import Prefix, SESSION_CACHE_TTL
from .model import MessageCache
from ..client import RedisClient
from ...common import BackendError, NotFoundError
from ..._db.crud.read import get_chat_messages_by_session
from ..._db.model import ChatMessage


async def get_message_count(session_id: str) -> int:
    key = Prefix.session(session_id)
    return await RedisClient.llen(key)


async def push_message(session_id: str, msg: MessageCache) -> None:
    key = Prefix.session(session_id)

    async with RedisClient.pipeline() as pipe:
        pipe.rpush(key, msg.model_dump_json())
        pipe.expire(key, SESSION_CACHE_TTL)


async def push_messages(session_id: str, msg_list: list[ChatMessage]) -> None:
    key = Prefix.session(session_id)

    async with RedisClient.pipeline() as pipe:
        for msg in msg_list:
            pipe.rpush(key, msg.model_dump_json())

        pipe.expire(key, SESSION_CACHE_TTL)


async def _get_messages(session_id: str) -> Optional[list[MessageCache]]:
    key = Prefix.session(session_id)

    async with RedisClient.pipeline(auto_execute=False) as pipe:
        pipe.lrange(key, 0, -1)
        pipe.expire(key, SESSION_CACHE_TTL)

    result = await pipe.execute()

    if len(result) != 2:
        raise BackendError()

    ans: list[str] = result[0]
    if not (ans and isinstance(ans, list)):
        return None

    return [MessageCache.model_validate_json(i) for i in ans]


async def read_message_cache(session_id: str) -> list[MessageCache]:
    msg = await _get_messages(session_id)
    if msg is not None:
        return msg

    data = await to_thread(get_chat_messages_by_session, session_id)
    if not data:
        raise NotFoundError

    await push_messages(session_id, data)
    return [MessageCache(role=i.role, content=i.content) for i in data]
