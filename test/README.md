```bash
# 需要额外安装 pytest
pip install pytest==9.1.1
pip install pytest-asyncio

pip install -e .
python -m pytest test/ -v
```

Redis 测试会读取当前工作路径下的 `test.env`：

`redis_manager` fixture 会在每条测试前后执行 `FLUSHDB`。必须使用专用测试
Redis 实例，不能填写开发或生产 Redis 配置。
