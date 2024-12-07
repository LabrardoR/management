"""
存放用户相关工具函数
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from app.models.user import User
import random
import time
import re
from app.utils.redis import get_redis

redis_client = get_redis()


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


async def get_code(phone: str, REDIS_PATH: str):
    # 验证手机号格式
    phone_regex = re.compile(r"^1[3-9]\d{9}$")
    if not phone_regex.match(phone):
        raise HTTPException(status_code=400, detail="手机号格式不正确！")

    # 获取当前时间戳（单位：毫秒）
    timestamp = int(time.time() * 1000)
    # 使用时间戳的一部分与随机数结合
    seed = timestamp + random.randint(0, 9999)
    # 生成随机验证码
    code = (seed % 900000) + 100000

    # 存储验证码到Redis中
    result = redis_client.set(REDIS_PATH + phone, str(code), ex=300)  # 过期时间五分钟
    # todo 发送验证码到手机
    print(f"验证码发送到手机号 {phone}: {code}")
    return {"message": "验证码已发送！"}


# 验证码校验
async def check_code(code: str, phone: str, REDIS_PATH: str):
    redis_code = redis_client.get(REDIS_PATH + phone)
    print("check code")
    # 验证码校验
    if code != redis_code:
        raise HTTPException(status_code=400, detail="验证码错误！")
    ttl = redis_client.ttl(REDIS_PATH + phone)
    if ttl <= 0:
        raise HTTPException(status_code=400, detail="验证码已过期！")

    return True
