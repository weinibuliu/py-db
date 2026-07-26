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

Redis 连接生命周期与业务场景分别由不同模块负责：

```python
from db import RedisClient, SessionStore

redis_client = RedisClient()
sessions = SessionStore(redis_client.get())

await sessions.create(uid, access_token, refresh_token)
owner_uid = await sessions.verify_access(access_token)

await redis_client.close()
```
