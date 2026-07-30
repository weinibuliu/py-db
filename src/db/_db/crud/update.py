from typing import Optional

from sqlmodel import Session, select

from ..model import User, Class, ClassRecord
from ..model import UpdateUser, UpdateClass, UpdateClassRecord
from ...common import NotFoundError
from ..engine import write_session

# update_* 系列函数将提供除自增主键、逻辑主键外所有字段的更新接口
# 具体字段是否可变需要下游自行处理
# 不允许将值重新设回 NULL

# TODO: 考虑提供更具体、更业务的 update 接口
# TODO: 如批量更新等接口


def update_user(
    uid: str,
    data: UpdateUser,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(User).where(User.uid == uid)

        usr: Optional[User] = session.exec(stat).first()
        if usr is None:
            raise NotFoundError()

        usr.sqlmodel_update(data.model_dump(exclude_unset=True, exclude_none=True))


def update_class(
    id: int,
    data: UpdateClass,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(Class).where(Class.id == id)

        cls: Optional[Class] = session.exec(stat).first()
        if cls is None:
            raise NotFoundError()

        cls.sqlmodel_update(data.model_dump(exclude_unset=True, exclude_none=True))


def update_class_record(
    id: int,
    data: UpdateClassRecord,
    ss: Optional[Session] = None,
) -> None:
    with write_session(ss) as session:
        stat = select(ClassRecord).where(ClassRecord.id == id)

        record: Optional[ClassRecord] = session.exec(stat).first()
        if record is None:
            raise NotFoundError()

        record.sqlmodel_update(data.model_dump(exclude_unset=True, exclude_none=True))
