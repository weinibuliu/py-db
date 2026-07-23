from .engine import DBEngine as db
from .engine import create_engine, close_engine
from .model import Role, Gender
from .model import User, Class, ClassRecord, CreateUser, CreateClass, CreateClassRecord
from .model import UpdateUser, UpdateClass, UpdateClassRecord
from .model import UserStatus, ClassStatus, ClassRecordStatus
from .model import User, Class, ClassRecord
from .model import UserPublic

from .crud.create import (
    create_user,
    create_class,
    create_class_record,
    CreateStatus,
)
from .crud.read import (
    get_user,
    get_class,
    get_class_record,
    get_class_by_id,
    get_user_by_id,
    get_user_by_uid,
)
from .crud.update import update_user, update_class, update_class_record, UpdateStatus

get_session = db.session

__all__ = [
    "create_engine",
    "close_engine",
    "Role",
    "Gender",
    "User",
    "CreateUser",
    "Class",
    "CreateClass",
    "ClassRecord",
    "CreateClassRecord",
    "UpdateUser",
    "UpdateClass",
    "UpdateClassRecord",
    "UserStatus",
    "ClassStatus",
    "ClassRecordStatus",
    "get_user",
    "get_class",
    "get_class_by_id",
    "get_user_by_id",
    "get_user_by_uid",
    "get_class_record",
    "create_user",
    "create_class",
    "create_class_record",
    "update_user",
    "update_class",
    "update_class_record",
    "CreateStatus",
    "UpdateStatus",
    "get_session",
    # "BaseUser",
    # "BaseClass",
    # "BaseClassRecord",
    "UserPublic",
]
