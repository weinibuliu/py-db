USER_PREFIX = "USR:"
USER_PROFILE_PREFIX = "USR-P:"

USER_CACHE_TTL = 30 * 24 * 3600  # 30d
USER_PROFILE_TTL = 30 * 24 * 3600  # 30d

SESSION_CACHE_TTL = 2 * 3600  # 2h
SESSION_CACHE_LIST_LIMIT = 20


class Prefix:
    @staticmethod
    def user(uid: str) -> str:
        return f"{USER_PREFIX}{uid}"

    @staticmethod
    def profile(uid: str) -> str:
        return f"{USER_PROFILE_PREFIX}{uid}"

    @staticmethod
    def session(session_id: str):
        return f"CSS:{session_id}"
