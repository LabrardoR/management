"""
我的数字人接口
"""
import datetime
import os
import time

from fastapi import APIRouter

from .upload import save_file
from ..utils.json_web_token import decode_jwt
from ..utils.voice_get import get_train_vocie_result

api_my_voice = APIRouter()

@api_my_voice.post("/tts/{token}", summary="Create voice")
async def tts(audio_name: str, generate_text: str, token : str):
    data = await decode_jwt(token)

    AUDIO_DIR = f"./audio/{audio_name}"
    phone = data.get("phone")
    # 重命名文件
    new_name = f"{phone}_{int(time.time())}"  # 新文件名
    try:
        a=await get_train_vocie_result(new_name, AUDIO_DIR, generate_text)
        if a==1:
            return {"message": "生成声音成功"}

    except Exception as e:
        return {"message": "生成声音失败"}