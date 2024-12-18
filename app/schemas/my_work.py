"""
schemas/my_work.py
我的工作组数据模型
"""
from pydantic import BaseModel, EmailStr, UUID4, field_validator
from typing import Optional


class CreateCharacterRequest(BaseModel):
    video_name: str
    audio_name: str
    name: str