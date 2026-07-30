from pydantic import BaseModel

from ...common.define import Role, UserStatus


class UserCache(BaseModel):
    uid: str
    role: Role
    status: UserStatus
