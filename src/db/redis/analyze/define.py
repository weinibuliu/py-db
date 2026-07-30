ROUTE_COUNT_PREFIX = "path:"


def _route(route: str) -> str:
    return f"{ROUTE_COUNT_PREFIX}{route}"
