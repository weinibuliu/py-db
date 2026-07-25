from enum import IntEnum
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Integer, SQLModel

from .define import Role, Gender, MyBaseModel, UserStatus


class BaseUser(MyBaseModel):
    uid: str = Field(max_length=255, nullable=False)
    password: str = Field(max_length=255, nullable=False)

    status: UserStatus = Field(sa_type=Integer, default=UserStatus.OK, nullable=False)

    name: str = Field(max_length=255, nullable=False)
    role: Role = Field(sa_type=Integer, nullable=False)
    gender: Gender = Field(sa_type=Integer, nullable=False)
    college: str = Field(max_length=255, nullable=False)

    # nullable fields
    reason: Optional[str] = Field(default=None, max_length=255, nullable=True)

    # only for students
    grade: Optional[str] = Field(default=None, max_length=255, nullable=True)
    class_: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
        sa_column_kwargs={"name": "class"},
    )
    major: Optional[str] = Field(default=None, max_length=255, nullable=True)


class User(BaseUser, table=True):
    __tablename__ = "user_rft"  # type: ignore


class CreateUser(BaseModel):
    uid: str = Field(min_length=10, max_length=10, description="uid")
    password: str = Field(min_length=8, max_length=18, description="password")
    name: str = Field(min_length=2, description="name")
    role: Role = Field(default=Role.Student)
    gender: Gender
    college: str

    # only for status
    grade: Optional[str] = Field(default=None)
    class_: Optional[str] = Field(default=None)
    major: Optional[str] = Field(default=None)


class UpdateUser(MyBaseModel):
    password: Optional[str] = None
    status: Optional[UserStatus] = None
    name: Optional[str] = None
    role: Optional[Role] = None
    gender: Optional[Gender] = None
    college: Optional[str] = None
    reason: Optional[str] = None
    grade: Optional[str] = None
    class_: Optional[str] = None
    major: Optional[str] = None


class UserPublic(SQLModel, table=False):
    uid: str = Field(max_length=255, nullable=False)

    name: str = Field(max_length=255, nullable=False)
    role: Role = Field(sa_type=Integer, nullable=False)
    gender: Gender = Field(sa_type=Integer, nullable=False)
    college: str = Field(max_length=255, nullable=False)

    # only for students
    grade: Optional[str] = Field(default=None, max_length=255, nullable=True)
    class_: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
        sa_column_kwargs={"name": "class"},
    )
    major: Optional[str] = Field(default=None, max_length=255, nullable=True)
