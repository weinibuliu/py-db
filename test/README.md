```bash
# 需要额外安装 pytest
pip install pytest==9.1.1
pip install pytest-asyncio

pip install -e .
python -m pytest test/ -v
```

SQL 与 Redis 测试都会读取当前工作路径下的 `test.env`。SQL 测试使用
MySQL，以确保驱动、约束行为和异常码与生产环境一致。

`test.env` 需要包含：

```dotenv
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

REDIS_HOST=
REDIS_PORT=
REDIS_USER=
REDIS_PASSWORD=
```

SQL fixture 只读取 `test.env`，并会在每条 CRUD 测试前后删除并重建
`DB_NAME` 中的全部表，因此必须填写专用测试数据库，不能填写开发或生产数据库。

`redis` fixture 会在每条测试前后执行 `FLUSHDB`。必须使用专用测试
Redis 实例，不能填写开发或生产 Redis 配置。
