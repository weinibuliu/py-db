from typing import Mapping

from pydantic import BaseModel, Field

from ...common import _now


class TracebackDetail(BaseModel):
    method: str = Field(..., description="请求方法")
    route: str = Field(..., description="请求路径")
    address: str = Field(..., description="客户端主机地址")
    body: dict = Field(default_factory=dict, description="请求体 dict")
    query_params: Mapping = Field(..., description="查询参数 dict")
    path_params: Mapping = Field(..., description="路径参数 dict")
    created_at: int = Field(default_factory=_now)

    traceback_format: str = Field(..., description="完整堆栈信息")
