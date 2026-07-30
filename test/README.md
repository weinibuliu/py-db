```bash
# 需要额外安装 pytest
pip install pytest==9.1.1
pip install pytest-asyncio

pip install -e .
python -m pytest test/ -v
```

SQL 与 Redis 测试都会读取当前工作路径下的 `test.env`。SQL 测试使用 MySQL，以确保驱动、约束行为和异常码与生产环境一致。

`test.env` 需要包含：

```dotenv
DB_HOST=localhost
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

REDIS_HOST=localhost
REDIS_PORT=
REDIS_USER=
REDIS_PASSWORD=
```

> [!CAUTION]
> 单元测试中会执行删表操作，务必使用本地专属的 MySQL 与 Redis 测试实例，禁止在 `test.env` 中填入远程服务器实例。

> [!TIP]
> 对于本地测试，可以首先调用 `db.create_all()` 函数执行建表。