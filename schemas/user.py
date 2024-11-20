# 定义 Pydantic 验证模型
from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    account: str
    username: Optional[str] = None  # 用户名可选
    password: str
    phone: Optional[str] = None     # 电话可选
    email: Optional[str] = None     # 邮箱可选

class UserLogin(BaseModel):
    account: str
    password: str

class UserUpdate(BaseModel):
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    account: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None
    role: int