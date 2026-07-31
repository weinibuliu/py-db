from pydantic import BaseModel, Field

from ...common.define import ChatRole


class MessageCache(BaseModel):
    role: ChatRole = Field(...)
    content: str = Field(...)
