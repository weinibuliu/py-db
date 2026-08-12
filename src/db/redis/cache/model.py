from ...common.define import ChatRole

from typing import Optional

from pydantic import BaseModel, Field

from ...common.define import Role, Gender, UserStatus


class UserCache(BaseModel):
    uid: str
    role: Role
    status: UserStatus
    reason: Optional[str]


class UserProfileCache(BaseModel):
    uid: str
    role: Role
    status: UserStatus
    reason: Optional[str]

    name: str
    gender: Gender
    college: str

    grade: Optional[str] = Field(default=None)
    class_: Optional[str] = Field(default=None, alias="class")
    major: Optional[str] = Field(default=None)


class MessageCache(BaseModel):
    role: ChatRole = Field(...)
    content: str = Field(...)
