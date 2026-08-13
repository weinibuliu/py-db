from asyncio import to_thread
from typing import Optional

from ..model import Class, ClassRecord, ChatMessage, ChatSession, User
from ...common.define import ClassRecordStatus, ClassStatus, Role, UserStatus
from . import read


async def async_get_user_by_pk(id: str) -> Optional[User]:
    return await to_thread(read.get_user_by_pk, id)


async def async_get_user_by_uid(uid: str) -> Optional[User]:
    return await to_thread(read.get_user_by_uid, uid)


async def async_get_user(
    *,
    uid: Optional[str] = None,
    name: Optional[str] = None,
    role: Optional[Role] = None,
    status: UserStatus = UserStatus.OK,
) -> list[User]:
    return await to_thread(
        read.get_user,
        uid=uid,
        name=name,
        role=role,
        status=status,
    )


async def async_get_class_by_id(id: int) -> Optional[Class]:
    return await to_thread(read.get_class_by_id, id)


async def async_get_class(
    *,
    id: Optional[int] = None,
    name: Optional[str] = None,
    course: Optional[str] = None,
    status: ClassStatus = ClassStatus.OK,
    private: bool = False,
) -> list[Class]:
    return await to_thread(
        read.get_class,
        id=id,
        name=name,
        course=course,
        status=status,
        private=private,
    )


async def async_get_class_record_by_pk(id: int) -> Optional[ClassRecord]:
    return await to_thread(read.get_class_record_by_pk, id)


async def async_get_class_record_by_uid(uid: str) -> list[ClassRecord]:
    return await to_thread(read.get_class_record_by_uid, uid)


async def async_get_class_record(
    *,
    uid: Optional[str] = None,
    role: Optional[Role] = None,
    class_id: Optional[int] = None,
    status: ClassRecordStatus = ClassRecordStatus.OK,
) -> list[ClassRecord]:
    return await to_thread(
        read.get_class_record,
        uid=uid,
        role=role,
        class_id=class_id,
        status=status,
    )


async def async_get_chat_session_by_id(
    session_id: str,
) -> Optional[ChatSession]:
    return await to_thread(read.get_chat_session_by_id, session_id)


async def async_get_chat_session_by_pk(id: str) -> Optional[ChatSession]:
    return await to_thread(read.get_chat_session_by_pk, id)


async def async_get_chat_session_by_uid(uid: str) -> list[ChatSession]:
    return await to_thread(read.get_chat_session_by_uid, uid)


async def async_get_chat_message_by_id(
    message_id: str,
) -> Optional[ChatMessage]:
    return await to_thread(read.get_chat_message_by_id, message_id)


async def async_get_chat_message_by_pk(id: str) -> Optional[ChatMessage]:
    return await to_thread(read.get_chat_message_by_pk, id)


async def async_get_chat_messages_by_session(
    session_id: str,
) -> list[ChatMessage]:
    return await to_thread(read.get_chat_messages_by_session, session_id)


__all__ = [
    "async_get_user_by_pk",
    "async_get_user_by_uid",
    "async_get_user",
    "async_get_class_by_id",
    "async_get_class",
    "async_get_class_record_by_pk",
    "async_get_class_record_by_uid",
    "async_get_class_record",
    "async_get_chat_session_by_id",
    "async_get_chat_session_by_pk",
    "async_get_chat_session_by_uid",
    "async_get_chat_message_by_id",
    "async_get_chat_message_by_pk",
    "async_get_chat_messages_by_session",
]
