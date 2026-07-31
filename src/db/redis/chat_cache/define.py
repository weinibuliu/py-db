SESSION_CACHE_TTL = 2 * 3600  # 2h
SESSION_CACHE_LIST_LIMIT = 10


class Prefix:
    @staticmethod
    def session(session_id: str):
        return f"CSS:{session_id}"
