import inspect

import pytest

from db._db.crud import async_read


PUBLIC_ASYNC_READS = (
    async_read.async_get_user_by_pk,
    async_read.async_get_user_by_uid,
    async_read.async_get_user,
    async_read.async_get_class_by_id,
    async_read.async_get_class,
    async_read.async_get_class_record_by_pk,
    async_read.async_get_class_record_by_uid,
    async_read.async_get_class_record,
    async_read.async_get_chat_session_by_id,
    async_read.async_get_chat_session_by_pk,
    async_read.async_get_chat_session_by_uid,
    async_read.async_get_chat_message_by_id,
    async_read.async_get_chat_message_by_pk,
    async_read.async_get_chat_messages_by_session,
)


@pytest.mark.parametrize("async_reader", PUBLIC_ASYNC_READS)
def test_async_readers_do_not_accept_session(async_reader: object) -> None:
    assert "ss" not in inspect.signature(async_reader).parameters


@pytest.mark.asyncio
async def test_async_reader_delegates_to_to_thread(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []

    async def run_in_thread(
        function: object,
        *args: object,
    ) -> str:
        calls.append((function, args))
        return "result"

    monkeypatch.setattr(async_read, "to_thread", run_in_thread)

    assert await async_read.async_get_user_by_pk("42") == "result"
    assert calls == [(async_read.read.get_user_by_pk, ("42",))]


@pytest.mark.asyncio
async def test_async_reader_forwards_keyword_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received: dict[str, object] = {}

    async def run_in_thread(
        function: object,
        *args: object,
        **kwargs: object,
    ) -> list[object]:
        assert function is async_read.read.get_user
        assert args == ()
        received.update(kwargs)
        return []

    monkeypatch.setattr(async_read, "to_thread", run_in_thread)

    assert await async_read.async_get_user(uid="user-1", name="User") == []
    assert received == {
        "uid": "user-1",
        "name": "User",
        "role": None,
        "status": async_read.UserStatus.OK,
    }
