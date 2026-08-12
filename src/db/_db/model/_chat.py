from typing import Optional

from sqlmodel import Field, TEXT
from sqlalchemy import Index

from ...common.define import MyBaseModel, ChatRole, ChatSessionStatus, ChatMessageStatus
from ...common.define import CreateBaseModel, UpdateBaseModel


# dto
class ChatSessionUpdate(UpdateBaseModel):
    status: Optional[ChatSessionStatus] = Field(default=None)
    title: Optional[str] = Field(default=None)
    message_count: Optional[int] = Field(default=None)
    total_tokens: Optional[int] = Field(default=None)
    # summary: Optional[str] = Field(default=None)


class ChatSessionCreate(CreateBaseModel):
    session_id: str = Field(...)
    status: ChatSessionStatus = Field(...)
    uid: str = Field(..., max_length=255, nullable=False)

    title: str = Field(..., max_length=255)
    message_count: int = Field(default=0)
    total_tokens: int = Field(default=0)

    # summary: Optional[str] = Field(default=None, sa_type=TEXT)


class BaseChatSession(MyBaseModel[ChatSessionCreate, ChatSessionUpdate]):
    session_id: str = Field(...)
    status: ChatSessionStatus = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    title: str = Field(..., max_length=255)
    message_count: int = Field(default=0)
    total_tokens: int = Field(default=0)

    summary: Optional[str] = Field(default=None, sa_type=TEXT)


class ChatSession(BaseChatSession, table=True):
    __tablename__ = "chat_session"  # type: ignore
    __table_args__ = (
        Index("chat_session_uid_index", "uid"),
        # TODO: 建立时间戳降序索引
        # Index("chat_session_uid_edited_at_index", "uid", "edited_at"),
    )


class ChatMessageCreate(CreateBaseModel):
    # 使用自增主键进行排序
    session_id: str = Field(...)
    message_id: str = Field(...)
    uid: str = Field(max_length=255)
    status: ChatMessageStatus = Field(default=ChatMessageStatus.OK)

    role: ChatRole = Field(...)
    content: str = Field(..., sa_type=TEXT)

    # metadata
    model: str = Field(...)
    temperature: int = Field(...)
    top_k: int = Field(...)

    # 成本核算
    cached_tokens: int = Field(...)
    uncached_tokens: int = Field(...)
    output_tokens: int = Field(...)


class ChatMessageUpdate(UpdateBaseModel): ...


class BaseChatMessage(MyBaseModel[ChatMessageCreate, ChatMessageUpdate]):
    # 使用自增主键进行排序
    session_id: str = Field(...)
    message_id: str = Field(...)
    uid: str = Field(max_length=255, nullable=False)
    status: ChatMessageStatus = Field(default=ChatMessageStatus.OK)

    role: ChatRole = Field(...)
    content: str = Field(..., sa_type=TEXT)

    # metadata
    model: str = Field(...)
    temperature: int = Field(...)
    top_k: int = Field(...)

    # 成本核算
    cached_tokens: int = Field(...)
    uncached_tokens: int = Field(...)
    output_tokens: int = Field(...)


class ChatMessage(BaseChatMessage, table=True):
    __tablename__ = "chat_message"  # type: ignore
    __table_args__ = (
        Index("chat_message_uid_index", "uid"),
        Index("chat_message_status_index", "status"),
    )
