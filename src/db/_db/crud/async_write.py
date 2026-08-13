from asyncio import to_thread

from ..model import (
    ChatMessageCreate,
    ChatSessionCreate,
    ClassCreate,
    ClassRecordCreate,
    UserCreate,
)
from . import create


async def async_create_user(data: UserCreate) -> None:
    await to_thread(create.create_user, data)


async def async_create_class(data: ClassCreate) -> None:
    await to_thread(create.create_class, data)


async def async_create_class_record(data: ClassRecordCreate) -> None:
    await to_thread(create.create_class_record, data)


async def async_create_chat_session(data: ChatSessionCreate) -> None:
    await to_thread(create.create_chat_session, data)


async def async_create_chat_message(data: ChatMessageCreate) -> None:
    await to_thread(create.create_chat_message, data)


__all__ = [
    "async_create_user",
    "async_create_class",
    "async_create_class_record",
    "async_create_chat_session",
    "async_create_chat_message",
]
