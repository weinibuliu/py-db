"""
测试数据库基础设施：SQL 与 Redis 均使用 test.env 指定的专用实例，
确保测试 adapter 与生产环境一致，并让每条测试从干净状态开始。
"""

from pathlib import Path

import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from dotenv import dotenv_values
from sqlmodel import SQLModel, create_engine

from db._db.engine import DBEngine
from db.common import DBConfig, RedisConfig
from db.redis.client import RedisClient

TEST_ENV_PATH = Path.cwd() / "test.env"


def _required_test_value(values: dict[str, str | None], key: str) -> str:
    value = values.get(key)
    if not value:
        raise RuntimeError(f"{key} in test.env must not be empty")
    return value


def _db_test_config() -> DBConfig:
    """只从 test.env 构造专用 MySQL 测试配置。"""
    values = dotenv_values(TEST_ENV_PATH)

    # host = _required_test_value(values, "DB_HOST")
    host = "localhost"
    port_value = _required_test_value(values, "DB_PORT")
    name = _required_test_value(values, "DB_NAME")
    user = _required_test_value(values, "DB_USER")
    password = _required_test_value(values, "DB_PASSWORD")

    try:
        port = int(port_value)
    except ValueError as exc:
        raise RuntimeError("DB_PORT in test.env must be an integer") from exc

    return DBConfig(
        host=host,
        port=port,
        name=name,
        user=user,
        password=password,
    )


def _redis_test_config() -> RedisConfig:
    """只从 test.env 构造 Redis 测试配置。"""
    values = dotenv_values(TEST_ENV_PATH)

    # host = values.get("REDIS_HOST")
    host = "localhost"

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


@pytest.fixture(scope="session")
def mysql_test_engine():
    """创建与生产参数一致的专用 MySQL 测试引擎。"""
    config = _db_test_config()
    engine = create_engine(
        config.url,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def setup_test_db(monkeypatch, mysql_test_engine):
    """每次测试前重建专用 MySQL schema，测试后清理。"""
    SQLModel.metadata.drop_all(mysql_test_engine)
    SQLModel.metadata.create_all(mysql_test_engine)

    monkeypatch.setattr(DBEngine, "_engine", mysql_test_engine)

    yield

    SQLModel.metadata.drop_all(mysql_test_engine)


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
