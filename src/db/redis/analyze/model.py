from typing import Optional

from pydantic import BaseModel, Field


class TracebackDetail(BaseModel):
    route: str = Field(..., description="请求的路径")
    traceback_format: str = Field(..., description="完整堆栈信息")

    address: str = Field(..., description="客户端主机地址")

    body: dict = Field(default_factory=dict, description="请求体 dict")
    query_params: dict = Field(default_factory=dict, description="查询参数 dict")
    path_params: dict = Field(default_factory=dict, description="路径参数 dict")
