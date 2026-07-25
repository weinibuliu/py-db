from contextlib import contextmanager
from typing import Generator, Optional

import sqlmodel as sql
from sqlalchemy import Engine

from ..common import DBConfig


# 默认情况下 下游无需显式初始化数据库连接 而是在调用时自动懒加载
# 但生产环境下 调用方可以考虑自行调用 `create_engine` 以提前初始化 db
class DBEngine:
    _engine: Optional[Engine] = None
    _cfg = DBConfig()

    @classmethod
    def create_engine(cls) -> None:
        if cls._engine is None:
            cls._engine = sql.create_engine(
                url=cls._cfg.url,
                pool_pre_ping=True,
                pool_recycle=3600,
            )

    @classmethod
    def close_engine(cls) -> None:
        if cls._engine is None:
            return

        cls._engine.dispose()
        cls._engine = None

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._engine is None:
            cls.create_engine()

        assert cls._engine

        return cls._engine

    @classmethod
    @contextmanager
    def session(cls) -> Generator[sql.Session, None, None]:
        with sql.Session(cls.get_engine()) as _session:
            yield _session


create_engine = DBEngine.create_engine
close_engine = DBEngine.close_engine
