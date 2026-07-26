from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Integer

from .define import MyBaseModel, ClassStatus


class BaseClass(MyBaseModel):
    status: ClassStatus = Field(sa_type=Integer, default=ClassStatus.OK, nullable=False)

    name: str = Field(max_length=255, nullable=False)
    course: Optional[str] = Field(default=None, max_length=255, nullable=True)
    private: bool = Field(default=False, nullable=False)


class Class(BaseClass, table=True):
    __tablename__ = "class"  # type: ignore


class UpdateClass(MyBaseModel):
    status: Optional[ClassStatus] = None
    name: Optional[str] = None
    course: Optional[str] = None
    private: Optional[bool] = None


# dto
class CreateClass(BaseModel):
    model_config = {"strict": True}

    name: str = Field(...)
    course: Optional[str] = Field(default=None)
    status: ClassStatus = Field(default=ClassStatus.OK)
    private: bool = Field(default=False)
