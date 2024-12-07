# 定义 Pydantic 验证模型
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional


class UserRegister(BaseModel):
    username: str
    phone: str
    password: str
    code: str                       #验证码

class UserCodeLogin(BaseModel):
    phone: str
    code: str

class UserReset(BaseModel):
    phone: str
    password: str
    code: str

class UserPasswordLogin(BaseModel):
    account: str # 可能为手机号，也可能为账号
    password: str

class UserUpdate(BaseModel):
    id: UUID4
    username: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID4
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    points: Optional[int] = None
    gender: Optional[int] = None  # 对应数据库中的 smallint
    email: Optional[str] = None
    role: int

class UserConsultation(BaseModel):
    phone: str
    email: str
    message: str