from enum import IntEnum, StrEnum
from typing import Optional, Self, TypeVar, Generic, Literal

from pydantic import model_validator
from sqlmodel import Field, SQLModel

from .utils import _now


class Role(IntEnum):
    Student = 0
    Teacher = 1
    Admin = 2


class Gender(IntEnum):
    Male = 0
    Female = 1


class UserStatus(IntEnum):
    OK = 0
    Banned = 1  # 禁用 | reason 字段中说明原因

    Deleted = 100


class ClassStatus(IntEnum):
    OK = 0
    Created = 1
    Ended = 2

    Deleted = 100


class ClassRecordStatus(IntEnum):
    OK = 0

    Deleted = 100


class ChatSessionStatus(IntEnum):
    OK = 0
    Archived = 1

    Deleted = 100


class ChatRole(StrEnum):
    system = "system"
    assistant = "assistant"
    tool = "tool"
    user = "user"


ChatRoleLiteral = Literal["system", "assistant", "tool", "user"]


class ChatMessageStatus(IntEnum):
    OK = 0
    Interrupted = 1  # 中断 不应使用 仅作审计

    Deleted = 100


class CreateBaseModel(SQLModel):
    created_by: Optional[str] = Field(default=None, description="creator's uid")
    edited_by: Optional[str] = Field(default=None, description="editor's uid")

    @model_validator(mode="after")
    def set_editor(self) -> Self:
        self.edited_by = self.created_by
        return self


class UpdateBaseModel(SQLModel):
    edited_by: Optional[str] = Field(default=None, description="editor's uid")


CreateDTO = TypeVar("CreateDTO", bound=CreateBaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=UpdateBaseModel)


class MyBaseModel(SQLModel, Generic[CreateDTO, UpdateDTO]):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: int = Field(default_factory=_now)
    edited_at: int = Field(default_factory=_now, sa_column_kwargs={"onupdate": _now})

    created_by: Optional[str] = Field(default=None, description="creator's uid")
    edited_by: Optional[str] = Field(default=None, description="editor's uid")

    @classmethod
    def from_create(cls, dto: CreateDTO) -> Self:
        return cls.model_validate(dto)

    def apply_update(self, dto: UpdateDTO) -> Self:
        self.sqlmodel_update(dto.model_dump(exclude_none=True, exclude_unset=True))
        return self
