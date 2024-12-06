"""
AI工作组接口
"""

import datetime

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

from app.models.user import User
from app.schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate

import hashlib
import random
import re

from app.utils.metaverse import get_access_token
from app.utils.user import get_current_user
api_ai_work_group = APIRouter()

'''
一键生成:只需上传文字或配音，选择你的数字分身，即可生成口播视频。
高度拟真:数字分身表情自然，动作流畅，宛如真人出镜
节省成本:只需一次拍摄，大幅降低了视频制作成本和时间。
'''
@api_ai_work_group.post("/make_video", description="用数字分身创作视频")
async def make_video(token = Depends(get_access_token), current_user: User = Depends(get_current_user)):

    return {"message": "功能开发中"}


@api_ai_work_group.post("/search_text", description="爆款文案搜索")
async def search_text(request: Request):
    return {"message": "功能未开发"}


@api_ai_work_group.post("/account_style_evaluation", description="账号风格评估")
async def account_style_evaluation(request: Request):
    return {"message": "功能未开发"}


@api_ai_work_group.post("/text_rewriting", description="AI文案改写")
async def text_rewriting(request: Request):
    return {"message": "功能未开发"}
