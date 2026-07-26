"""
Session Redis Lua scripts.

All scripts assume a single-session-per-user model. Callers must pass fully
formatted Redis keys through ``KEYS``; raw tokens are never interpreted by Lua.
The current key scheme targets standalone Redis; Redis Cluster would require
all keys used by a script to share one hash slot.
"""

# /login
# 撤销旧 token 对 -> 创建新 access
NEW_SESSION = """
-- KEYS[1]: access index key for the user
-- KEYS[2]: refresh index key for the user
-- KEYS[3]: new access token key
-- KEYS[4]: optional new refresh token key
-- ARGV[1]: uid
-- ARGV[2]: access token TTL in seconds
-- ARGV[3]: optional refresh token TTL in seconds
--
-- KEYS[4] and ARGV[3] must either both be present or both be omitted.

local access_ttl = tonumber(ARGV[2])
local refresh_ttl = tonumber(ARGV[3])
local has_refresh = KEYS[4] ~= nil or ARGV[3] ~= nil

if not ARGV[1] or ARGV[1] == "" then
    return redis.error_reply("uid must not be empty")
end

if not access_ttl or access_ttl <= 0 or access_ttl % 1 ~= 0 then
    return redis.error_reply("access TTL must be a positive integer")
end

if has_refresh and (not KEYS[4] or not refresh_ttl) then
    return redis.error_reply("refresh token key and TTL must be provided together")
end

if refresh_ttl and (refresh_ttl <= 0 or refresh_ttl % 1 ~= 0) then
    return redis.error_reply("refresh TTL must be a positive integer")
end

local access_owner = redis.call("GET", KEYS[3])

if access_owner and access_owner ~= ARGV[1] then
    return redis.error_reply("access token already belongs to another user")
end

if has_refresh then
    local refresh_owner = redis.call("GET", KEYS[4])

    if refresh_owner and refresh_owner ~= ARGV[1] then
        return redis.error_reply("refresh token already belongs to another user")
    end
end

local old_access_key = redis.call("GET", KEYS[1])
local old_refresh_key = redis.call("GET", KEYS[2])

if old_access_key then
    redis.call("DEL", old_access_key)
end

if old_refresh_key then
    redis.call("DEL", old_refresh_key)
end

redis.call("DEL", KEYS[1], KEYS[2])

redis.call("SET", KEYS[3], ARGV[1], "EX", access_ttl)
redis.call("SET", KEYS[1], KEYS[3], "EX", access_ttl)

if has_refresh then
    redis.call("SET", KEYS[4], ARGV[1], "EX", refresh_ttl)
    redis.call("SET", KEYS[2], KEYS[4], "EX", refresh_ttl)
end

return 1
"""

# /logout
# 根据索引删除对应 token 及索引
DEL_SESSION = """
-- KEYS[1]: access index key for the user
-- KEYS[2]: refresh index key for the user

local access_key = redis.call("GET", KEYS[1])
local refresh_key = redis.call("GET", KEYS[2])
local deleted = redis.call("DEL", KEYS[1], KEYS[2])

if access_key then
    deleted = deleted + redis.call("DEL", access_key)
end

if refresh_key then
    deleted = deleted + redis.call("DEL", refresh_key)
end

return deleted
"""

# /refresh
# 确认 refresh_token 属于当前会话 -> 换发 access_token
REFRESH_SESSION = """
-- KEYS[1]: access index key for the user
-- KEYS[2]: refresh index key for the user
-- KEYS[3]: presented refresh token key
-- KEYS[4]: new access token key
-- ARGV[1]: uid
-- ARGV[2]: access token TTL in seconds

local access_ttl = tonumber(ARGV[2])

if not ARGV[1] or ARGV[1] == "" then
    return redis.error_reply("uid must not be empty")
end

if not access_ttl or access_ttl <= 0 or access_ttl % 1 ~= 0 then
    return redis.error_reply("access TTL must be a positive integer")
end

local refresh_uid = redis.call("GET", KEYS[3])
local current_refresh_key = redis.call("GET", KEYS[2])

if refresh_uid ~= ARGV[1] or current_refresh_key ~= KEYS[3] then
    return 0
end

local access_owner = redis.call("GET", KEYS[4])

if access_owner and access_owner ~= ARGV[1] then
    return redis.error_reply("access token already belongs to another user")
end

local old_access_key = redis.call("GET", KEYS[1])

if old_access_key then
    redis.call("DEL", old_access_key)
end

redis.call("SET", KEYS[4], ARGV[1], "EX", access_ttl)
redis.call("SET", KEYS[1], KEYS[4], "EX", access_ttl)

return 1
"""


__all__ = ["NEW_SESSION", "DEL_SESSION", "REFRESH_SESSION"]
