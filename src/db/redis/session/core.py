from typing import List, Optional, Union

from ..client import RedisClient
from .define import ACCESS_TTL, REFRESH_TTL, Prefix
from .scripts import DEL_SESSION, NEW_SESSION, REFRESH_SESSION


async def verify_access(token: str) -> Optional[str]:
    if not token:
        raise ValueError("token must not be empty")

    return await RedisClient.get(name=Prefix.access(token))


async def verify_refresh(token: str) -> Optional[str]:
    if not token:
        raise ValueError("token must not be empty")

    return await RedisClient.get(name=Prefix.refresh(token))


async def _run_script(
    script: str,
    keys: List[str],
    args: List[Union[str, int]],
) -> int:
    result = await RedisClient.eval(script, len(keys), *keys, *args)
    if type(result) is not int:
        raise TypeError(
            f"Redis Lua script returned {type(result).__name__}, expected int"
        )
    return result


async def create(
    uid: str,
    access_token: str,
    refresh_token: Optional[str] = None,
) -> bool:
    """Revoke the old session and create a new one."""
    if not uid:
        raise ValueError("uid must not be empty")
    if not access_token:
        raise ValueError("access_token must not be empty")
    if refresh_token == "":
        raise ValueError("refresh_token must not be empty")

    keys = [
        Prefix.access_idx(uid),
        Prefix.refresh_idx(uid),
        Prefix.access(access_token),
    ]
    args: List[Union[str, int]] = [uid, ACCESS_TTL]

    if refresh_token is not None:
        keys.append(Prefix.refresh(refresh_token))
        args.append(REFRESH_TTL)

    return await _run_script(NEW_SESSION, keys, args) == 1


async def revoke(uid: str) -> int:
    """Revoke the current session and return the deleted key count."""
    if not uid:
        raise ValueError("uid must not be empty")

    return await _run_script(
        DEL_SESSION,
        [Prefix.access_idx(uid), Prefix.refresh_idx(uid)],
        [],
    )


async def refresh(
    uid: str,
    refresh_token: str,
    new_access_token: str,
) -> bool:
    """Validate the refresh token and atomically replace the access token."""
    if not uid:
        raise ValueError("uid must not be empty")
    if not refresh_token:
        raise ValueError("refresh_token must not be empty")
    if not new_access_token:
        raise ValueError("new_access_token must not be empty")

    return (
        await _run_script(
            REFRESH_SESSION,
            [
                Prefix.access_idx(uid),
                Prefix.refresh_idx(uid),
                Prefix.refresh(refresh_token),
                Prefix.access(new_access_token),
            ],
            [uid, ACCESS_TTL],
        )
        == 1
    )
