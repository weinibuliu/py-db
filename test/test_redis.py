import asyncio

import pytest


@pytest.mark.asyncio
async def test_login_without_remember_me_revokes_previous_session(redis_manager):
    uid = "user-1"

    assert await redis_manager.new_session(uid, "old-access", "old-refresh") is True
    assert await redis_manager.new_session(uid, "new-access") is True

    assert await redis_manager.verify_access_token("new-access") == uid
    assert await redis_manager.verify_access_token("old-access") is None
    assert await redis_manager.verify_refresh_token("old-refresh") is None


@pytest.mark.asyncio
async def test_remembered_login_creates_access_and_refresh(redis_manager):
    uid = "user-1"

    created = await redis_manager.new_session(uid, "access-1", "refresh-1")

    assert created is True
    assert await redis_manager.verify_access_token("access-1") == uid
    assert await redis_manager.verify_refresh_token("refresh-1") == uid


@pytest.mark.asyncio
async def test_refresh_replaces_only_access_token(redis_manager):
    uid = "user-1"
    await redis_manager.new_session(uid, "access-1", "refresh-1")

    refreshed = await redis_manager.refresh_session(uid, "refresh-1", "access-2")

    assert refreshed is True
    assert await redis_manager.verify_access_token("access-1") is None
    assert await redis_manager.verify_access_token("access-2") == uid
    assert await redis_manager.verify_refresh_token("refresh-1") == uid


@pytest.mark.asyncio
async def test_stale_refresh_cannot_modify_current_session(redis_manager):
    uid = "user-1"
    await redis_manager.new_session(uid, "access-1", "refresh-1")
    await redis_manager.new_session(uid, "access-2", "refresh-2")

    refreshed = await redis_manager.refresh_session(uid, "refresh-1", "access-3")

    assert refreshed is False
    assert await redis_manager.verify_access_token("access-2") == uid
    assert await redis_manager.verify_access_token("access-3") is None
    assert await redis_manager.verify_refresh_token("refresh-2") == uid


@pytest.mark.asyncio
async def test_logout_revokes_current_session_and_is_idempotent(redis_manager):
    uid = "user-1"
    await redis_manager.new_session(uid, "access-1", "refresh-1")

    deleted = await redis_manager.del_session(uid)

    assert deleted == 4
    assert await redis_manager.verify_access_token("access-1") is None
    assert await redis_manager.verify_refresh_token("refresh-1") is None
    assert await redis_manager.del_session(uid) == 0


@pytest.mark.asyncio
async def test_concurrent_logout_and_refresh_cannot_restore_session(redis_manager):
    uid = "user-1"
    await redis_manager.new_session(uid, "access-1", "refresh-1")

    await asyncio.gather(
        redis_manager.refresh_session(uid, "refresh-1", "access-2"),
        redis_manager.del_session(uid),
    )

    assert await redis_manager.verify_access_token("access-1") is None
    assert await redis_manager.verify_access_token("access-2") is None
    assert await redis_manager.verify_refresh_token("refresh-1") is None
