# 定义 Pydantic 验证模型
from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    phone: str
    code: str                       #验证码

class UserCodeLogin(BaseModel):
    phone: str
    code: str

class UserReset(BaseModel):
    phone: str
    password: str
    code: str

class UserPasswordLogin(BaseModel):
    phone: str
    password: str

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    account: str
    username: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None
    role: int