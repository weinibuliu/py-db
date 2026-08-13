from asyncio import to_thread

from ..model import ChatSessionUpdate, ClassRecordUpdate, ClassUpdate, UserUpdate
from . import update


async def async_update_user(uid: str, data: UserUpdate) -> None:
    await to_thread(update.update_user, uid, data)


async def async_update_class(id: int, data: ClassUpdate) -> None:
    await to_thread(update.update_class, id, data)


async def async_update_class_record(id: int, data: ClassRecordUpdate) -> None:
    await to_thread(update.update_class_record, id, data)


async def async_update_chat_session(
    session_id: str,
    data: ChatSessionUpdate,
) -> None:
    await to_thread(update.update_chat_session, session_id, data)


__all__ = [
    "async_update_user",
    "async_update_class",
    "async_update_class_record",
    "async_update_chat_session",
]
