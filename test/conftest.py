"""
测试数据库基础设施：SQL 使用 SQLite 内存数据库，Redis 使用 test.env
指定的专用实例，确保每条测试从干净状态开始。
"""

from pathlib import Path

import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from dotenv import dotenv_values
from sqlmodel import SQLModel, create_engine

from src.db._db.engine import DBEngine
from src.db.common import RedisConfig
from src.db._redis.client import RedisClient

TEST_ENV_PATH = Path.cwd() / "test.env"


def _redis_test_config() -> RedisConfig:
    """只从 test.env 构造 Redis 配置，避免误用根目录 .env。"""
    values = dotenv_values(TEST_ENV_PATH)

    host = values.get("REDIS_HOST")
    if not host:
        raise RuntimeError("REDIS_HOST in test.env must not be empty")

    try:
        port = int(values["REDIS_PORT"])  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise RuntimeError("REDIS_PORT in test.env must be an integer") from exc

    return RedisConfig(
        host=host,
        port=port,
        user=values.get("REDIS_USER"),
        password=values.get("REDIS_PASSWORD"),
    )


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """每次测试前创建全新的 SQLite 内存数据库，测试后销毁。"""
    engine = create_engine("sqlite://", echo=False)

    # 创建所有 SQLModel 注册的表
    SQLModel.metadata.create_all(engine)

    # 绕过 MySQL 连接：DBEngine.get_engine() 发现 _engine 非 None 会直接返回
    monkeypatch.setattr(DBEngine, "_engine", engine)

    yield

    # 测试后清理
    SQLModel.metadata.drop_all(engine)


@pytest_asyncio.fixture
async def redis(monkeypatch):
    """连接专用测试 Redis，并在每条测试前后清空 DB 0。"""
    config = _redis_test_config()
    pool = aioredis.ConnectionPool(
        host=config.host,
        port=config.port,
        username=config.user,
        password=config.password,
        db=0,
        max_connections=10,
        decode_responses=True,
    )
    client = aioredis.Redis(connection_pool=pool, protocol=2)
    ready = False

    try:
        await client.ping()
        await client.flushdb()
        ready = True
        monkeypatch.setattr(RedisClient, "_client", client)
        yield
    finally:
        if ready:
            await client.flushdb()
        await RedisClient.close()
