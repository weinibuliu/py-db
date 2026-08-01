from typing import Optional

from sqlmodel import Session

from ..engine import write_session
from ..model import User, UserCreate
from ..model import Class, ClassCreate
from ..model import ClassRecord, ClassRecordCreate
from ..model import ChatSession, ChatSessionCreate, ChatMessage, ChatMessageCreate


def create_user(
    data: UserCreate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(User.from_create(data))


def create_class(
    data: ClassCreate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(Class.from_create(data))


def create_class_record(
    data: ClassRecordCreate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ClassRecord.from_create(data))


def create_chat_session(
    data: ChatSessionCreate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ChatSession.from_create(data))


def create_chat_message(
    data: ChatMessageCreate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ChatMessage.from_create(data))
