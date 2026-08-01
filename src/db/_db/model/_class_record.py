from typing import Optional

from sqlmodel import Field, Integer
from sqlalchemy import Index

from ...common.define import MyBaseModel, Role, ClassRecordStatus
from ...common.define import CreateBaseModel, UpdateBaseModel


# dto
class ClassRecordUpdate(UpdateBaseModel):
    status: Optional[ClassRecordStatus] = Field(default=None)
    uid: Optional[str] = Field(default=None)
    role: Optional[Role] = Field(default=None)
    class_id: Optional[int] = Field(default=None)


class ClassRecordCreate(CreateBaseModel):
    uid: str = Field(..., min_length=10, max_length=10, description="uid")
    role: Role = Field(...)
    class_id: int = Field(...)
    status: ClassRecordStatus = ClassRecordStatus.OK


# define
class BaseClassRecord(MyBaseModel[ClassRecordCreate, ClassRecordUpdate]):
    status: ClassRecordStatus = Field(
        sa_type=Integer,
        default=ClassRecordStatus.OK,
        nullable=False,
    )

    uid: str = Field(max_length=255, nullable=False)
    role: Role = Field(sa_type=Integer, nullable=False)
    class_id: int = Field(nullable=False)  # 即 class.id


class ClassRecord(BaseClassRecord, table=True):
    """ClassRecord Table"""

    __tablename__ = "class_record"  # type: ignore
    __table_args__ = (
        Index("class_record_uid_class_id_uindex", "uid", "class_id", unique=True),
        # Index("class_record_uid_index", "uid"),
        Index("class_record_status_index", "status"),
        Index("class_record_role_index", "role"),
        Index("class_record_class_id_index", "class_id"),
        Index("class_record_created_by_index", "created_by"),
    )
