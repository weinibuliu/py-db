# Sync Cache

db 侧发生 CREATE/UPDATE 时，同步更新 Redis 侧缓存

当下游需要查表时，首先从 redis 侧读取缓存，如果 redis 未能返回数据，自动 fallback 到数据库查询，然后将新值回写到 redis 中。

提供一个统一的 load_cache 函数（名称待定，但行为一致）

## 同步策略
同步策略为：变更时删除缓存，产生新读取时重建缓存。

当 db 发生更改时，成功 commit 更改后， **DELETE** redis 中的缓存键。

当实际发生读取时，下游尝试 load_cache。此时，发现 redis 侧无缓存，fallback 到查表，将 **SET** 操作加入队列，然后立即返回所需数据。
