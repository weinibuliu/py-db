from typing import Optional

from sqlmodel import Field, Integer, SQLModel
from sqlalchemy import Index

from ...common.define import Role, Gender, MyBaseModel, UserStatus, DTOBaseModel


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
    """User Table"""

    __tablename__ = "user_rft"  # type: ignore

    __table_args__ = (
        Index("user_uid_uindex", "uid", unique=True),
        Index("user_rft_status_index", "status"),
        Index("user_rft_name_index", "name"),
        Index("user_rft_role_index", "role"),
        Index("user_rft_created_by_index", "created_by"),
    )


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


# dto
class UpdateUser(DTOBaseModel):
    password: Optional[str] = Field(default=None)
    status: Optional[UserStatus] = Field(default=None)
    name: Optional[str] = Field(default=None)
    role: Optional[Role] = Field(default=None)
    gender: Optional[Gender] = Field(default=None)
    college: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    grade: Optional[str] = Field(default=None)
    class_: Optional[str] = Field(default=None)
    major: Optional[str] = Field(default=None)


class CreateUser(DTOBaseModel):
    uid: str = Field(..., min_length=10, max_length=10, description="uid")
    password: str = Field(..., description="encrypt password")
    name: str = Field(..., min_length=2, description="name")
    role: Role = Field(default=Role.Student)
    gender: Gender = Field(...)
    college: str = Field(...)

    # only for status
    grade: Optional[str] = Field(default=None)
    class_: Optional[str] = Field(default=None)
    major: Optional[str] = Field(default=None)
