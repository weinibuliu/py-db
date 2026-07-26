import asyncio

import pytest

from src.db._redis import (
    create_session,
    refresh_session,
    revoke_session,
    verify_access,
    verify_refresh,
)


pytestmark = pytest.mark.usefixtures("redis")


@pytest.mark.asyncio
async def test_login_without_remember_me_revokes_previous_session():
    uid = "user-1"

    assert await create_session(uid, "old-access", "old-refresh") is True
    assert await create_session(uid, "new-access") is True

    assert await verify_access("new-access") == uid
    assert await verify_access("old-access") is None
    assert await verify_refresh("old-refresh") is None


@pytest.mark.asyncio
async def test_remembered_login_creates_access_and_refresh():
    uid = "user-1"

    created = await create_session(uid, "access-1", "refresh-1")

    assert created is True
    assert await verify_access("access-1") == uid
    assert await verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_refresh_replaces_only_access_token():
    uid = "user-1"
    await create_session(uid, "access-1", "refresh-1")

    refreshed = await refresh_session(uid, "refresh-1", "access-2")

    assert refreshed is True
    assert await verify_access("access-1") is None
    assert await verify_access("access-2") == uid
    assert await verify_refresh("refresh-1") == uid


@pytest.mark.asyncio
async def test_stale_refresh_cannot_modify_current_session():
    uid = "user-1"
    await create_session(uid, "access-1", "refresh-1")
    await create_session(uid, "access-2", "refresh-2")

    refreshed = await refresh_session(uid, "refresh-1", "access-3")

    assert refreshed is False
    assert await verify_access("access-2") == uid
    assert await verify_access("access-3") is None
    assert await verify_refresh("refresh-2") == uid


@pytest.mark.asyncio
async def test_logout_revokes_current_session_and_is_idempotent():
    uid = "user-1"
    await create_session(uid, "access-1", "refresh-1")

    deleted = await revoke_session(uid)

    assert deleted == 4
    assert await verify_access("access-1") is None
    assert await verify_refresh("refresh-1") is None
    assert await revoke_session(uid) == 0


@pytest.mark.asyncio
async def test_concurrent_logout_and_refresh_cannot_restore_session():
    uid = "user-1"
    await create_session(uid, "access-1", "refresh-1")

    await asyncio.gather(
        refresh_session(uid, "refresh-1", "access-2"),
        revoke_session(uid),
    )

    assert await verify_access("access-1") is None
    assert await verify_access("access-2") is None
    assert await verify_refresh("refresh-1") is None
