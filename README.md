# python-database

本模块旨在为项目提供一套可重用的，便于拓展的基础设施，包含：

- SQL 数据库交互
- Redis 交互

## 设计原则

- 使用 SQL ORM
- 为下游提供清晰、明确的类型注解
- 封装业务需求，可能避免下游自行封装

## Python

> 包名为 `db`

### 直接安装

```bash
# 在项目根目录下
pip install -e py-db

# 在子项目中
pip install -e ../py-db

# 或者使用绝对路径
pip install -e /path/to/py-db
```

### 在 requirements.txt 中添加

```bash
# requirements.txt (使用相对于 requirements.txt 文件所在的相对目录)
# ...
-e ../py-db

# bash
pip install -r requirements.txt
```

然后可以 import 使用

```python
import db
# ...
```

Redis 与 SQL 数据库采用相同的模块级调用方式。FastAPI lifespan 只负责连接生命周期：

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import close_redis, create_redis, create_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_redis()
    try:
        yield
    finally:
        await close_redis()


app = FastAPI(lifespan=lifespan)


async def login():
    await create_session(
        uid,
        access_token,
        refresh_token,
    )
```
