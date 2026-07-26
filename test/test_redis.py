import asyncio

import pytest


@pytest.mark.asyncio
async def test_login_without_remember_me_revokes_previous_session(session_store):
    uid = "user-1"

    assert await session_store.create(uid, "old-access", "old-refresh") is True
    assert await session_store.create(uid, "new-access") is True

    assert await session_store.verify_access("new-access") == uid
    assert await session_store.verify_access("old-access") is None
    assert await session_store.verify_refresh("old-refresh") is None


@pytest.mark.asyncio
async def test_remembered_login_creates_access_and_refresh(session_store):
    uid = "user-1"

    created = await session_store.create(uid, "access-1", "refresh-1")

    assert created is True
    assert await session_store.verify_access("access-1") == uid
    assert await session_store.verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_refresh_replaces_only_access_token(session_store):
    uid = "user-1"
    await session_store.create(uid, "access-1", "refresh-1")

    refreshed = await session_store.refresh(uid, "refresh-1", "access-2")

    assert refreshed is True
    assert await session_store.verify_access("access-1") is None
    assert await session_store.verify_access("access-2") == uid
    assert await session_store.verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_stale_refresh_cannot_modify_current_session(session_store):
    uid = "user-1"
    await session_store.create(uid, "access-1", "refresh-1")
    await session_store.create(uid, "access-2", "refresh-2")

    refreshed = await session_store.refresh(uid, "refresh-1", "access-3")

    assert refreshed is False
    assert await session_store.verify_access("access-2") == uid
    assert await session_store.verify_access("access-3") is None
    assert await session_store.verify_refresh("refresh-2") == uid


@pytest.mark.asyncio
async def test_logout_revokes_current_session_and_is_idempotent(session_store):
    uid = "user-1"
    await session_store.create(uid, "access-1", "refresh-1")

    deleted = await session_store.revoke(uid)

    assert deleted == 4
    assert await session_store.verify_access("access-1") is None
    assert await session_store.verify_refresh("refresh-1") is None
    assert await session_store.revoke(uid) == 0


@pytest.mark.asyncio
async def test_concurrent_logout_and_refresh_cannot_restore_session(session_store):
    uid = "user-1"
    await session_store.create(uid, "access-1", "refresh-1")

    await asyncio.gather(
        session_store.refresh(uid, "refresh-1", "access-2"),
        session_store.revoke(uid),
    )

    assert await session_store.verify_access("access-1") is None
    assert await session_store.verify_access("access-2") is None
    assert await session_store.verify_refresh("refresh-1") is None
