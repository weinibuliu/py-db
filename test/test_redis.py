import asyncio

import pytest

from db.redis import session

pytestmark = pytest.mark.usefixtures("redis")


@pytest.mark.asyncio
async def test_login_without_remember_me_revokes_previous_session():
    uid = "user-1"

    assert await session.create(uid, "old-access", "old-refresh") is True
    assert await session.create(uid, "new-access") is True

    assert await session.verify_access("new-access") == uid
    assert await session.verify_access("old-access") is None
    assert await session.verify_refresh("old-refresh") is None


@pytest.mark.asyncio
async def test_remembered_login_creates_access_and_refresh():
    uid = "user-1"

    created = await session.create(uid, "access-1", "refresh-1")

    assert created is True
    assert await session.verify_access("access-1") == uid
    assert await session.verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_refresh_replaces_only_access_token():
    uid = "user-1"
    await session.create(uid, "access-1", "refresh-1")

    refreshed = await session.refresh(uid, "refresh-1", "access-2")

    assert refreshed is True
    assert await session.verify_access("access-1") is None
    assert await session.verify_access("access-2") == uid
    assert await session.verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_stale_refresh_cannot_modify_current_session():
    uid = "user-1"
    await session.create(uid, "access-1", "refresh-1")
    await session.create(uid, "access-2", "refresh-2")

    refreshed = await session.refresh(uid, "refresh-1", "access-3")

    assert refreshed is False
    assert await session.verify_access("access-2") == uid
    assert await session.verify_access("access-3") is None
    assert await session.verify_refresh("refresh-2") == uid


@pytest.mark.asyncio
async def test_logout_revokes_current_session_and_is_idempotent():
    uid = "user-1"
    await session.create(uid, "access-1", "refresh-1")

    deleted = await session.revoke(uid)

    assert deleted == 4
    assert await session.verify_access("access-1") is None
    assert await session.verify_refresh("refresh-1") is None
    assert await session.revoke(uid) == 0


@pytest.mark.asyncio
async def test_concurrent_logout_and_refresh_cannot_restore_session():
    uid = "user-1"
    await session.create(uid, "access-1", "refresh-1")

    await asyncio.gather(
        session.refresh(uid, "refresh-1", "access-2"),
        session.revoke(uid),
    )

    assert await session.verify_access("access-1") is None
    assert await session.verify_access("access-2") is None
    assert await session.verify_refresh("refresh-1") is None
