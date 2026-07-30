from contextlib import nullcontext
from typing import Optional

from sqlmodel import Session, select

from ..engine import DBEngine as db
from ..model import User
from ..model import Class, ClassStatus
from ..model import ClassRecord
from ...common.define import UserStatus, ClassRecordStatus, Role


def get_user_by_id(id: str, ss: Optional[Session] = None) -> Optional[User]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(User).where(User.id == id)
        return session.exec(stat).first()


def get_user_by_uid(uid: str, ss: Optional[Session] = None) -> Optional[User]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(User).where(User.uid == uid)
        return session.exec(stat).first()


def get_user(
    *,
    name: Optional[str] = None,
    role: Optional[Role] = None,
    status: UserStatus = UserStatus.OK,
    ss: Optional[Session] = None,
) -> list[User]:
    """
    NOTE: `name` `role` 为 None 代表不参与查询
    """

    with db.session() if ss is None else nullcontext(ss) as session:
        conditions: list[bool] = []

        if name is not None:
            conditions.append(User.name == name)
        if role is not None:
            conditions.append(User.role == role)
        if status is not None:
            conditions.append(User.status == status)

        stat = select(User).where(*conditions)
        return list(session.exec(stat).all())


def get_class_by_id(id: int, ss: Optional[Session] = None) -> Optional[Class]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(Class).where(Class.id == id)
        return session.exec(stat).first()


def get_class(
    *,
    name: Optional[str] = None,
    course: Optional[str] = None,
    status: ClassStatus = ClassStatus.OK,
    private: bool = False,
    ss: Optional[Session] = None,
) -> list[Class]:
    """
    NOTE: `name` `course` 为 None 代表不参与查询
    """

    with db.session() if ss is None else nullcontext(ss) as session:
        conditions: list[bool] = []

        if name is not None:
            conditions.append(Class.name == name)
        if course is not None:
            conditions.append(Class.course == course)

        conditions.append(Class.status == status)
        conditions.append(Class.private == private)

        stat = select(Class).where(*conditions)
        return list(session.exec(stat).all())


def get_class_record_by_uid(
    uid: str, ss: Optional[Session] = None
) -> list[ClassRecord]:
    with db.session() if ss is None else nullcontext(ss) as session:
        stat = select(ClassRecord).where(ClassRecord.uid == uid)
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
