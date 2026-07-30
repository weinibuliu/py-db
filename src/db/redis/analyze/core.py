from ..client import RedisClient
from .define import _route


async def route_count(path: str):
    await RedisClient.incr(_route(path))
