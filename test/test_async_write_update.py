import inspect

import pytest

from db._db.crud import async_update, async_write
from db._db.model import ClassCreate, ClassUpdate


PUBLIC_ASYNC_WRITES = (
    async_write.async_create_user,
    async_write.async_create_class,
    async_write.async_create_class_record,
    async_write.async_create_chat_session,
    async_write.async_create_chat_message,
)

PUBLIC_ASYNC_UPDATES = (
    async_update.async_update_user,
    async_update.async_update_class,
    async_update.async_update_class_record,
    async_update.async_update_chat_session,
)


@pytest.mark.parametrize(
    "async_operation",
    PUBLIC_ASYNC_WRITES + PUBLIC_ASYNC_UPDATES,
)
def test_async_writes_and_updates_do_not_accept_session(
    async_operation: object,
) -> None:
    assert "ss" not in inspect.signature(async_operation).parameters


@pytest.mark.asyncio
async def test_async_create_delegates_to_to_thread(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []
    data = ClassCreate(name="Class")

    async def run_in_thread(function: object, *args: object) -> None:
        calls.append((function, args))

    monkeypatch.setattr(async_write, "to_thread", run_in_thread)

    await async_write.async_create_class(data)

    assert calls == [(async_write.create.create_class, (data,))]


@pytest.mark.asyncio
async def test_async_update_delegates_to_to_thread(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []
    data = ClassUpdate(name="Renamed")

    async def run_in_thread(function: object, *args: object) -> None:
        calls.append((function, args))

    monkeypatch.setattr(async_update, "to_thread", run_in_thread)

    await async_update.async_update_class(42, data)

    assert calls == [(async_update.update.update_class, (42, data))]
