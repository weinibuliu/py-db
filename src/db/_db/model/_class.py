from typing import Optional

from sqlmodel import Field, Integer
from sqlalchemy import Index

from .define import MyBaseModel, ClassStatus, DTOBaseModel


class BaseClass(MyBaseModel):
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


# dto
class UpdateClass(DTOBaseModel):
    status: Optional[ClassStatus] = None
    name: Optional[str] = None
    course: Optional[str] = None
    private: Optional[bool] = None


class CreateClass(DTOBaseModel):
    name: str = Field(...)
    course: Optional[str] = Field(default=None)
    status: ClassStatus = Field(default=ClassStatus.OK)
    private: bool = Field(default=False)
