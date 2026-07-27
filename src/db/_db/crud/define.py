from enum import IntEnum


class CreateStatus(IntEnum):
    OK = 0
    Partially = 1  # only a part of data successes

    Existed = 100

    Unknown = 500
    ValueError = 501


class UpdateStatus(IntEnum):
    OK = 0

    PrimaryKeyNotFound = 1  # 按自增主键查找未找到结果
    NotFound = 2  # 按逻辑(不一定是逻辑主键)查找未找到结果
    Multiple = 3  # 按逻辑查找到多个对象 无法具体到单条记录

    Unknown = 500
