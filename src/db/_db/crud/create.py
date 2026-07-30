from typing import Optional

from sqlmodel import Session

from ..model import User
from ..model import CreateUser, CreateClass, CreateClassRecord
from ..model import Class, ClassRecord
from ..engine import write_session


def create_user(
    usr: CreateUser,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        session.add(User(**usr.model_dump()))


def create_class(
    cls: CreateClass,
    ss: Optional[Session] = None,
) -> None:
    auto_commit = ss is None
    with write_session(ss) as session:
        session.add(Class(**cls.model_dump()))


def create_class_record(
    record: CreateClassRecord,
    ss: Optional[Session] = None,
) -> None:
    auto_commit = ss is None
    with write_session(ss) as session:
        session.add(ClassRecord(**record.model_dump()))
