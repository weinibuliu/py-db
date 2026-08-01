from typing import Optional

from sqlmodel import Field, Integer
from sqlalchemy import Index

from ...common.define import MyBaseModel, ClassStatus
from ...common.define import CreateBaseModel, UpdateBaseModel


# dto
class ClassUpdate(UpdateBaseModel):
    status: Optional[ClassStatus] = Field(default=None)
    name: Optional[str] = Field(default=None)
    course: Optional[str] = Field(default=None)
    private: Optional[bool] = Field(default=None)


class ClassCreate(CreateBaseModel):
    name: str = Field(...)
    course: Optional[str] = Field(default=None)
    status: ClassStatus = Field(default=ClassStatus.OK)
    private: bool = Field(default=False)


# define
class BaseClass(MyBaseModel[ClassCreate, ClassUpdate]):
    status: ClassStatus = Field(sa_type=Integer, default=ClassStatus.OK, nullable=False)

    name: str = Field(max_length=255, nullable=False)
    course: Optional[str] = Field(default=None, max_length=255, nullable=True)
    private: bool = Field(default=False, nullable=False)


class Class(BaseClass, table=True):
    """Class Table"""

    __tablename__ = "class"  # type: ignore
    __table_args__ = (
        Index(
            "class_name_course_status_uindex", "name", "course", "status", unique=True
        ),
        Index("class_status_index", "status"),
        Index("class_name_index", "name"),
        Index("class_course_index", "course"),
        Index("class_private_index", "private"),
        Index("class_created_by_index", "created_by"),
    )
