from contextlib import contextmanager
from typing import Generator, Optional

import sqlmodel as sql
from sqlmodel import Session
from sqlalchemy import Engine, exc

from ..common import (
    DBConfig,
    DBError,
    AlreadyExistsError,
    BackendError,
    BackendTimeoutError,
    BackendUnavailableError,
    DataIntegrityError,
)
from .utils import is_unique_violation


# 默认情况下 下游无需显式初始化数据库连接 而是在调用时自动懒加载
# 但生产环境下 调用方可以考虑自行调用 `create_engine` 以提前初始化 db
class DBEngine:
    _engine: Optional[Engine] = None

    @classmethod
    def create_engine(cls) -> None:
        if cls._engine is None:
            _cfg = DBConfig()
            cls._engine = sql.create_engine(
                url=_cfg.url,
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

    @classmethod
    @contextmanager
    def write_session(
        cls,
        ss: Optional[Session] = None,
    ) -> Generator[Session, None, None]:
        """管理 session 生命周期"""

        try:
            if ss is None:
                with cls.session() as session:
                    yield session
                    session.commit()
            else:
                yield ss
                ss.flush()

        # except DBError as e:
        #     raise e

        except exc.IntegrityError as e:
            if is_unique_violation(e):
                raise AlreadyExistsError() from e
            raise DataIntegrityError() from e

        except exc.TimeoutError as e:
            raise BackendTimeoutError() from e

        except exc.DBAPIError as e:
            if e.connection_invalidated:
                raise BackendUnavailableError() from e

            raise BackendError() from e

        except exc.SQLAlchemyError as e:
            raise BackendError() from e

    @classmethod
    def create_all_table(cls):
        """!!!ONLY FOR DEV MODE!!!"""
        sql.SQLModel.metadata.create_all(cls.get_engine())


create_engine = DBEngine.create_engine
close_engine = DBEngine.close_engine
get_session = DBEngine.session
write_session = DBEngine.write_session
create_all = DBEngine.create_all_table
