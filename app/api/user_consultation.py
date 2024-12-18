"""
客户咨询接口
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

import hashlib
import random
import re

from app.models.user import User
from app.models.user_form import UserForm
from app.schemas.user import UserConsultation
from app.utils.user import get_current_user

api_consultation = APIRouter()


@api_consultation.post("/send",description="留言功能")
async def sendMessages(user_consultation : UserConsultation, user : User = Depends(get_current_user)):
    phone = user_consultation.phone
    email = user_consultation.email
    message = user_consultation.message
    user_id = user.id
    if message is None or phone is None or email is None:
        raise HTTPException(status_code=403, detail="请将信息补充完整！")
    new_user_form  = UserForm.create(
        phone = phone,
        email = email,
        message = message,
        user_id = user_id
    )
    return {
        "message": "发送咨询表单成功！",
    }

