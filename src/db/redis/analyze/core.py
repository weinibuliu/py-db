from typing import Optional, overload

from ..client import RedisClient
from .define import Prefix, TOTAL_COUNT_KEY, TRACEBACK_TTL
from .model import TracebackDetail
from ...common import NotFoundError


async def route_count(method: str, route: str):
    async with RedisClient.pipeline() as pipe:
        pipe.incr(TOTAL_COUNT_KEY)
        pipe.incr(Prefix.route(method, route))


async def get_total_route_count() -> Optional[str]:
    return await RedisClient.get(TOTAL_COUNT_KEY)


async def get_route_count(method: str, route: str) -> Optional[str]:
    return await RedisClient.get(Prefix.route(method, route))


async def add_traceback(_uuid: str, detail: TracebackDetail):
    await RedisClient.set(
        Prefix.traceback(_uuid),
        detail.model_dump_json(),
        TRACEBACK_TTL,
    )


async def get_traceback(_uuid: str) -> TracebackDetail:
    tb = await RedisClient.get(
        Prefix.traceback(_uuid),
    )

    if tb is None:
        raise NotFoundError()
    return TracebackDetail.model_validate_json(tb)
