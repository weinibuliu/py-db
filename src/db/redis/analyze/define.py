TOTAL_COUNT_KEY = "path:total"
ROUTE_COUNT_PREFIX = "path:"
TRACEBACK_PREFIX = "tb:"

TRACEBACK_TTL = 7 * 24 * 3600  # 7d


class Prefix:
    @staticmethod
    def route(method: str, route: str) -> str:
        return f"A:{method}-{ROUTE_COUNT_PREFIX}{route}"

    @staticmethod
    def traceback(_uuid: str) -> str:
        return f"{TRACEBACK_PREFIX}{_uuid}"
