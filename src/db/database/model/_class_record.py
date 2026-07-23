from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel, Integer

from .common import MyBaseModel, Role


class ClassRecordStatus(IntEnum):
    OK = 0

    Deleted = 100  # 逻辑删除


class BaseClassRecord(MyBaseModel):
    status: ClassRecordStatus = Field(
        sa_type=Integer,
        default=ClassRecordStatus.OK,
        nullable=False,
    )

    uid: str = Field(max_length=255, nullable=False)
    role: Role = Field(sa_type=Integer, nullable=False)
    class_id: int = Field(nullable=False)  # 即 class.id


class ClassRecord(BaseClassRecord, table=True):
    __tablename__ = "class_record"  # type: ignore


class CreateClassRecord(MyBaseModel):
    uid: str
    role: Role
    class_id: int
    status: ClassRecordStatus = ClassRecordStatus.OK


class UpdateClassRecord(MyBaseModel):
    status: Optional[ClassRecordStatus] = None
    uid: Optional[str] = None
    role: Optional[Role] = None
    class_id: Optional[int] = None
