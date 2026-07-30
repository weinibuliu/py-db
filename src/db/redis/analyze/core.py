from ..client import RedisClient
from .define import _route, TOTAL_COUNT_KEY


async def route_count(route: str):
    async with RedisClient.pipeline() as pipe:
        pipe.incr(TOTAL_COUNT_KEY)
        pipe.incr(_route(route))
