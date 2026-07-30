ACCESS_TTL = 12 * 3600  # 12h
REFRESH_TTL = 30 * 24 * 3600  # 30d

ACCESS_PREFIX = "ACC:"
REFRESH_PREFIX = "REF:"

ACCESS_IDX_PREFIX = "u_acc:"
REFRESH_IDX_PREFIX = "u_ref:"


def _access(token: str) -> str:
    return f"{ACCESS_PREFIX}{token}"


def _refresh(token: str) -> str:
    return f"{REFRESH_PREFIX}{token}"


def _access_idx(uid: str) -> str:
    return f"{ACCESS_IDX_PREFIX}{uid}"


def _refresh_idx(uid: str) -> str:
    return f"{REFRESH_IDX_PREFIX}{uid}"


__all__ = [
    "ACCESS_TTL",
    "REFRESH_TTL",
    "_access",
    "_refresh",
    "_access_idx",
    "_refresh_idx",
]
