import asyncio

import pytest

from db.common import NotFoundError
from db.common.define import ChatRole
from db.redis.cache import MessageCache, chat
from db.redis.cache.define import Prefix, SESSION_CACHE_TTL
from db.redis.client import RedisClient

pytestmark = pytest.mark.usefixtures("redis")


def _message(content: str, role: ChatRole = ChatRole.user) -> MessageCache:
    return MessageCache(role=role, content=content)


@pytest.mark.asyncio
async def test_session_cache_returns_pushed_messages_in_order() -> None:
    messages = [
        _message("question"),
        _message("answer", ChatRole.assistant),
    ]

    for message in messages:
        await chat.push_message("session-1", message)

    assert await chat.read_message_cache("session-1") == messages


@pytest.mark.asyncio
async def test_session_cache_returns_every_pushed_message() -> None:
    messages = [_message(f"message-{index}") for index in range(12)]

    for message in messages:
        await chat.push_message("session-1", message)

    assert await chat.read_message_cache("session-1") == messages


@pytest.mark.asyncio
async def test_session_caches_are_isolated() -> None:
    first_message = _message("first")
    second_message = _message("second", ChatRole.system)

    await chat.push_message("session-1", first_message)
    await chat.push_message("session-2", second_message)

    assert await chat.read_message_cache("session-1") == [first_message]
    assert await chat.read_message_cache("session-2") == [second_message]


@pytest.mark.asyncio
async def test_missing_session_raises_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(chat, "get_chat_messages_by_session", lambda _: [])

    with pytest.raises(NotFoundError):
        await chat.read_message_cache("missing-session")


@pytest.mark.asyncio
async def test_cache_miss_reads_database_and_populates_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    messages = [
        _message("question"),
        _message("answer", ChatRole.assistant),
    ]
    database_reads = 0

    def read_database(_: str) -> list[MessageCache]:
        nonlocal database_reads
        database_reads += 1
        return messages

    monkeypatch.setattr(chat, "get_chat_messages_by_session", read_database)

    assert await chat.read_message_cache("session-1") == messages
    assert await chat.read_message_cache("session-1") == messages
    assert database_reads == 1


@pytest.mark.asyncio
async def test_concurrent_pushes_do_not_lose_messages() -> None:
    # The test Redis pool allows 10 checked-out connections. Keep this test
    # concurrent without turning it into a connection-pool exhaustion test.
    messages = [_message(f"message-{index}") for index in range(8)]

    await asyncio.gather(
        *(chat.push_message("session-1", message) for message in messages)
    )

    cached_messages = await chat.read_message_cache("session-1")
    assert len(cached_messages) == len(messages)
    assert {message.content for message in cached_messages} == {
        message.content for message in messages
    }


@pytest.mark.asyncio
async def test_push_refreshes_session_ttl() -> None:
    client = RedisClient.get_client()
    key = Prefix.session("session-1")
    await chat.push_message("session-1", _message("first"))
    await client.expire(key, 1)

    await chat.push_message("session-1", _message("second"))

    assert SESSION_CACHE_TTL - 1 <= await client.ttl(key) <= SESSION_CACHE_TTL


@pytest.mark.asyncio
async def test_read_refreshes_session_ttl() -> None:
    client = RedisClient.get_client()
    key = Prefix.session("session-1")
    message = _message("message")
    await chat.push_message("session-1", message)
    await client.expire(key, 1)

    assert await chat.read_message_cache("session-1") == [message]
    assert SESSION_CACHE_TTL - 1 <= await client.ttl(key) <= SESSION_CACHE_TTL
