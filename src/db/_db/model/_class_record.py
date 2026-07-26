from typing import Optional

from sqlmodel import Field, Integer
from pydantic import BaseModel

from .define import MyBaseModel, Role, ClassRecordStatus


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


class UpdateClassRecord(MyBaseModel):
    status: Optional[ClassRecordStatus] = None
    uid: Optional[str] = None
    role: Optional[Role] = None
    class_id: Optional[int] = None


# dto
class CreateClassRecord(BaseModel):
    model_config = {"strict": True}

    uid: str = Field(..., min_length=10, max_length=10, description="uid")
    role: Role = Field(...)
    class_id: int = Field(...)
    status: ClassRecordStatus = ClassRecordStatus.OK
