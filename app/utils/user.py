"""
存放用户相关工具函数
"""
import datetime

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

from app.models.user import User
from app.schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate

import hashlib
import random
import re


async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 示例：根据 session_id 查找用户 -> 可按需更改为使用 Redis 或数据库
    user_id = session_id.split("_")[1]  # session_id 格式为 "session_<user_id>"
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="会话无效，请重新登录")

    return user


async def check_current_user(phone : str, code : str, redis_ : redis.StrictRedis):
