# LLM Chat Cache

存储会话对应的 message cache 缓存

调用方应当将写表操作移至后台任务中 避免阻塞接口返回

考虑到实际应用场景 给予一个较短的的默认 TTL (2h) 每次 push / read 时刷新 TTL

Redis Key: CSS:{session_id}

> CSS: Chat Session
