from typing import Optional

from sqlmodel import Field, TEXT
from sqlalchemy import Index

from ...common.define import MyBaseModel, ChatRole


class BaseChatSession(MyBaseModel):
    session_id: str = Field(...)
    uid: str = Field(max_length=255, nullable=False)

    title: str = Field(..., max_length=255)
    message_count: int = Field(default=0)
    total_tokens: int = Field(default=0)

    summary: Optional[str] = Field(default=None, sa_type=TEXT)


class BaseChatMessage(MyBaseModel):
    # 使用自增主键进行排序
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
    __table_args__ = [
        Index("chat_session_uid_index", "uid"),
        # TODO: 建立时间戳降序索引
        # Index("chat_session_uid_edited_at_index", "uid", "edited_at"),
    ]


class ChatMessage(BaseChatMessage, table=True):
    __tablename__ = "chat_message"  # type: ignore
    __table_args__ = [
        Index("chat_message_uid_index", "uid"),
    ]
