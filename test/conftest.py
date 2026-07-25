"""
将 DBEngine 重定向到 SQLite 内存数据库，
确保每次测试在干净的表结构上运行，不污染真实数据库。
"""

import pytest
from sqlmodel import SQLModel, create_engine

from src.db._db.engine import DBEngine


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
