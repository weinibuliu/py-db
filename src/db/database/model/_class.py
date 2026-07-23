from enum import IntEnum
from typing import Optional

from sqlmodel import Field, Integer

from .common import MyBaseModel


class ClassStatus(IntEnum):
    OK = 0
    Created = 1
    Ended = 2

    Deleted = 100  # 逻辑删除


class BaseClass(MyBaseModel):
    status: ClassStatus = Field(sa_type=Integer, default=ClassStatus.OK, nullable=False)

    name: str = Field(max_length=255, nullable=False)
    course: Optional[str] = Field(default=None, max_length=255, nullable=True)
    private: bool = Field(default=False, nullable=False)


class Class(BaseClass, table=True):
    __tablename__ = "class"  # type: ignore


class CreateClass(MyBaseModel):
    name: str
    course: Optional[str] = None
    status: ClassStatus = ClassStatus.OK
    private: bool = False


class UpdateClass(MyBaseModel):
    status: Optional[ClassStatus] = None
    name: Optional[str] = None
    course: Optional[str] = None
    private: Optional[bool] = None
