from typing import Any
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """
    响应数据模型
    """
    code: int = 2000
    message: str = "success"
    data: Any = None
