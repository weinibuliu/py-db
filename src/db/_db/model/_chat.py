from typing import Optional

from sqlmodel import Field, TEXT
from sqlalchemy import Index

from ...common.define import MyBaseModel, ChatRole, DTOBaseModel, ChatSessionStatus


class BaseChatSession(MyBaseModel):
    session_id: str = Field(...)
    status: ChatSessionStatus = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    title: str = Field(..., max_length=255)
    message_count: int = Field(default=0)
    total_tokens: int = Field(default=0)

    summary: Optional[str] = Field(default=None, sa_type=TEXT)


class BaseChatMessage(MyBaseModel):
    # 使用自增主键进行排序
    session_id: str = Field(...)
    message_id: str = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    role: ChatRole = Field(...)
    content: str = Field(..., sa_type=TEXT)

    # metadata
    model: str = Field(...)
    temperature: int = Field(...)
    top_k: int = Field(...)

    # 成本核算
    input_tokens: int = Field(...)
    output_tokens: int = Field(...)


class ChatSession(BaseChatSession, table=True):
    __tablename__ = "chat_session"  # type: ignore
    __table_args__ = (
        Index("chat_session_uid_index", "uid"),
        # TODO: 建立时间戳降序索引
        # Index("chat_session_uid_edited_at_index", "uid", "edited_at"),
    )


class ChatMessage(BaseChatMessage, table=True):
    __tablename__ = "chat_message"  # type: ignore
    __table_args__ = (Index("chat_message_uid_index", "uid"),)


# dto
class UpdateChatSession(DTOBaseModel):
    status: Optional[ChatSessionStatus] = Field(default=None)
    title: Optional[str] = Field(default=None)
    message_count: Optional[int] = Field(default=None)
    total_tokens: Optional[int] = Field(default=None)
    summary: Optional[str] = Field(default=None)


class UpdateChatMessage: ...


class CreateChatSession(DTOBaseModel):
    session_id: str = Field(...)
    status: ChatSessionStatus = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    title: str = Field(..., max_length=255)
    message_count: int = Field(default=0)
    total_tokens: int = Field(default=0)

    summary: Optional[str] = Field(default=None, sa_type=TEXT)


class CreateChatMessage(DTOBaseModel):
    # 使用自增主键进行排序
    session_id: str = Field(...)
    message_id: str = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    role: ChatRole = Field(...)
    content: str = Field(..., sa_type=TEXT)

    # metadata
    model: str = Field(...)
    temperature: int = Field(...)
    top_k: int = Field(...)

    # 成本核算
    input_tokens: int = Field(...)
    output_tokens: int = Field(...)
