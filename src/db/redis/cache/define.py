USER_PREFIX = "USR:"

USER_CACHE_TTL = 30 * 24 * 3600  # 30d


def user(uid: str) -> str:
    return f"{USER_PREFIX}{uid}"
