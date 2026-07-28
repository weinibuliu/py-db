class DBError(Exception):
    """db 库所有运行期错误的基类。"""

    code: int = 500


class AlreadyExistsError(DBError):
    """创建的数据已经存在。"""

    code: int = 409


class NotFoundError(DBError):
    """命令操作的目标不存在。"""

    code: int = 404


class BackendError(DBError):
    """SQL/Redis 后端执行失败。"""


class BackendUnavailableError(BackendError):
    """后端无法连接或连接中断。"""


class BackendTimeoutError(BackendError):
    """连接池或后端操作超时。"""


class DataIntegrityError(BackendError):
    """未能归类为明确业务冲突的数据约束错误。"""


class BackendProtocolError(BackendError):
    """后端返回了不符合预期的数据。"""


class ConfigurationError(DBError):
    """数据库或 Redis 配置无效。"""


class UnknownError(DBError):
    """未知错误 来自 Python 内部"""
