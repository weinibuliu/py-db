from contextlib import nullcontext
from typing import Optional

from sqlmodel import Session, select

from ..engine import DBEngine as db
from ..model import User
from ..model import Class, CreateUser, CreateClass, CreateClassRecord
from ..model import ClassRecord
from .define import CreateStatus


def create_user(
    usr: CreateUser,
    ss: Optional[Session] = None,
) -> CreateStatus:
    auto_commit = ss is None
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(User).where(User.uid == usr.uid)
        if session.exec(stat).first() is not None:
            return CreateStatus.Existed

        session.add(User(**usr.model_dump()))

        if auto_commit:
            session.commit()
        else:
            session.flush()
        return CreateStatus.OK


def create_class(
    cls: CreateClass,
    ss: Optional[Session] = None,
) -> CreateStatus:
    auto_commit = ss is None
    with db.session() if ss is None else nullcontext(ss) as session:
        session.add(Class(**cls.model_dump()))

        if auto_commit:
            session.commit()
        else:
            session.flush()
        return CreateStatus.OK


def create_class_record(
    record: CreateClassRecord,
    ss: Optional[Session] = None,
):
    auto_commit = ss is None
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ClassRecord).where(
            ClassRecord.uid == record.uid,
            ClassRecord.class_id == record.class_id,
        )
        if session.exec(stat).first() is not None:
            return CreateStatus.Existed

        session.add(ClassRecord(**record.model_dump()))

        if auto_commit:
            session.commit()
        else:
            session.flush()
        return CreateStatus.OK
