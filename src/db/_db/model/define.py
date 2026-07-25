from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel

from ...common import _now


class Role(IntEnum):
    Student = 0
    Teacher = 1
    Admin = 2


class Gender(IntEnum):
    Male = 0
    Female = 1


class UserStatus(IntEnum):
    OK = 0
    Banned = 1  # 禁用 | reason 字段中说明原因

    Deleted = 100


class ClassStatus(IntEnum):
    OK = 0
    Created = 1
    Ended = 2

    Deleted = 100


class ClassRecordStatus(IntEnum):
    OK = 0

    Deleted = 100




class MyBaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)

    created_at: int = Field(default_factory=_now)
    edited_at: int = Field(default_factory=_now, sa_column_kwargs={"onupdate": _now})

    created_by: Optional[str] = Field(default=None, description="creator's uid")
