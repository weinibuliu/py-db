from contextlib import nullcontext
from typing import Optional

from sqlmodel import Session, select

from ..engine import DBEngine as db
from ..model import User
from ..model import Class, ClassStatus
from ..model import ClassRecord
from ..model import ChatSession
from ..model import ChatMessage
from ...common.define import (
    UserStatus,
    ClassRecordStatus,
    Role,
    ChatMessageStatus,
    ChatSessionStatus,
)

"""
NOTE:
    对于存在业务主键的查询:
    id 指的是业务主键而非 pk 即 get_*_by_id = get_*_by_*_id
    如果需要使用 pk 查询，请使用 get_*_by_pk 函数

    对于依赖业务主键的查询，会强制返回状态为 OK(0) 的项
    如有需要，请使用 get_* 函数进行查询
"""


def get_user_by_pk(id: str, ss: Optional[Session] = None) -> Optional[User]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(User).where(User.id == id)
        return session.exec(stat).first()


def get_user_by_uid(
    uid: str,
    ss: Optional[Session] = None,
) -> Optional[User]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(User).where(User.uid == uid, User.status == UserStatus.OK)
        return session.exec(stat).first()


def get_user(
    *,
    uid: Optional[str] = None,
    name: Optional[str] = None,
    role: Optional[Role] = None,
    status: UserStatus = UserStatus.OK,
    ss: Optional[Session] = None,
) -> list[User]:
    """
    NOTE: `uid` `name` `role` 为 None 代表不参与查询
    """

    with db.session() if ss is None else nullcontext(ss) as session:
        conditions: list[bool] = []

        if uid is not None:
            conditions.append(User.uid == uid)
        if name is not None:
            conditions.append(User.name == name)
        if role is not None:
            conditions.append(User.role == role)
        if status is not None:
            conditions.append(User.status == status)

        stat = select(User).where(*conditions)
        return list(session.exec(stat).all())


def get_class_by_id(
    id: int,
    ss: Optional[Session] = None,
) -> Optional[Class]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(Class).where(Class.id == id, Class.status == ClassStatus.OK)
        return session.exec(stat).first()


def get_class(
    *,
    id: Optional[int] = None,
    name: Optional[str] = None,
    course: Optional[str] = None,
    status: ClassStatus = ClassStatus.OK,
    private: bool = False,
    ss: Optional[Session] = None,
) -> list[Class]:
    """
    NOTE: `id` `name` `course` 为 None 代表不参与查询
    """

    with db.session() if ss is None else nullcontext(ss) as session:
        conditions: list[bool] = []

        if id is not None:
            conditions.append(Class.id == id)
        if name is not None:
            conditions.append(Class.name == name)
        if course is not None:
            conditions.append(Class.course == course)

        conditions.append(Class.status == status)
        conditions.append(Class.private == private)

        stat = select(Class).where(*conditions)
        return list(session.exec(stat).all())


def get_class_record_by_pk(
    id: int,
    ss: Optional[Session] = None,
) -> Optional[ClassRecord]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ClassRecord).where(ClassRecord.id == id)
        return session.exec(stat).first()


def get_class_record_by_uid(
    uid: str, ss: Optional[Session] = None
) -> list[ClassRecord]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ClassRecord).where(
            ClassRecord.uid == uid,
            ClassRecord.status == ClassRecordStatus.OK,
        )
        return list(session.exec(stat).all())


def get_class_record(
    *,
    uid: Optional[str] = None,
    role: Optional[Role] = None,
    class_id: Optional[int] = None,
    status: ClassRecordStatus = ClassRecordStatus.OK,
    ss: Optional[Session] = None,
) -> list[ClassRecord]:
    """
    NOTE: `uid` `role` `class_id` 为 None 代表不参与查询
    """

    with db.session() if ss is None else nullcontext(ss) as session:
        conditions: list[bool] = []

        if uid is not None:
            conditions.append(ClassRecord.uid == uid)
        if role is not None:
            conditions.append(ClassRecord.role == role)
        if class_id is not None:
            conditions.append(ClassRecord.class_id == class_id)

        conditions.append(ClassRecord.status == status)

        stat = select(ClassRecord).where(*conditions)
        return list(session.exec(stat).all())


def get_chat_session_by_id(
    session_id: str,
    ss: Optional[Session] = None,
) -> Optional[ChatSession]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatSession).where(ChatSession.session_id == session_id)
        return session.exec(stat).first()


def get_chat_session_by_pk(
    id: str,
    ss: Optional[Session] = None,
) -> Optional[ChatSession]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatSession).where(ChatSession.id == id)
        return session.exec(stat).first()


def get_chat_session_by_uid(
    uid: str,
    ss: Optional[Session] = None,
) -> list[ChatSession]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatSession).where(
            ChatSession.uid == uid,
            ChatSession.status == ChatSessionStatus.OK,
        )
        return list(session.exec(stat).all())


def get_chat_message_by_id(
    message_id: str,
    ss: Optional[Session] = None,
) -> Optional[ChatMessage]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatMessage).where(ChatMessage.message_id == message_id)
        return session.exec(stat).first()


def get_chat_message_by_pk(
    id: str,
    ss: Optional[Session] = None,
) -> Optional[ChatMessage]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatMessage).where(ChatMessage.id == id)
        return session.exec(stat).first()


def get_chat_messages_by_session(
    session_id: str,
    ss: Optional[Session] = None,
) -> list[ChatMessage]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ChatMessage).where(
            ChatMessage.session_id == session_id,
            ChatMessage.status == ChatMessageStatus.OK,
        )
        return list(session.exec(stat).all())
