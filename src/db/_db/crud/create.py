from typing import Optional

from sqlmodel import Session

from ..engine import write_session
from ..model import User, CreateUser
from ..model import Class, CreateClass
from ..model import ClassRecord, CreateClassRecord
from ..model import ChatSession, CreateChatSession, ChatMessage, CreateChatMessage


def create_user(
    data: CreateUser,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(User(**data.model_dump()))


def create_class(
    data: CreateClass,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(Class(**data.model_dump()))


def create_class_record(
    data: CreateClassRecord,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ClassRecord(**data.model_dump()))


def create_chat_session(
    data: CreateChatSession,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ChatSession(**data.model_dump()))


def create_chat_message(
    data: CreateChatMessage,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(ChatMessage(**data.model_dump()))
