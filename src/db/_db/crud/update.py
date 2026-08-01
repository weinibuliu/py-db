from typing import Optional

from sqlmodel import Session, select

from ..model import User, UserUpdate
from ..model import Class, ClassUpdate
from ..model import ClassRecord, ClassRecordUpdate
from ..model import ChatSession, ChatSessionUpdate
from ...common import NotFoundError
from ..engine import write_session

# update_* 系列函数将提供除自增主键、逻辑主键外所有字段的更新接口
# 具体字段是否可变需要下游自行处理
# 不允许将值重新设回 NULL

# TODO: 考虑提供更具体、更业务的 update 接口
# TODO: 如批量更新等接口


def update_user(
    uid: str,
    data: UserUpdate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(User).where(User.uid == uid)

        entity: Optional[User] = session.exec(stat).first()
        if entity is None:
            raise NotFoundError()

        entity.apply_update(data)


def update_class(
    id: int,
    data: ClassUpdate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(Class).where(Class.id == id)

        entity: Optional[Class] = session.exec(stat).first()
        if entity is None:
            raise NotFoundError()

        entity.apply_update(data)


def update_class_record(
    id: int,
    data: ClassRecordUpdate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(ClassRecord).where(ClassRecord.id == id)

        entity: Optional[ClassRecord] = session.exec(stat).first()
        if entity is None:
            raise NotFoundError()

        entity.apply_update(data)


def update_chat_session(
    session_id: str,
    data: ChatSessionUpdate,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(ChatSession).where(ChatSession.session_id == session_id)

        entity: Optional[ChatSession] = session.exec(stat).first()
        if entity is None:
            raise NotFoundError()

        entity.apply_update(data)
