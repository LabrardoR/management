"""
我的作品接口接口
"""
import os

from app.models.user import User
from app.utils.user import get_current_user
from fastapi import APIRouter, HTTPException, Depends, Request, Response, UploadFile, File, HTTPException
from tortoise.exceptions import IntegrityError
from app.config import SERVER_ADDRESS, SERVER_PORT
import time

api_upload = APIRouter()

@api_upload.post("/audio", description="上传音频文件")
async def upload_audio(request : Request, current_user : User = Depends(get_current_user), file: UploadFile = File(...)):
    AUDIO_DIR = "./audio"
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    # 重命名文件
    new_name = f"{current_user.phone}_{int(time.time())}.mp3"  # 新文件名

    # 保存文件到指定目录
    file_path = await save_file(file, AUDIO_DIR, new_name)

    try:
        # 返回相对路径或可直接访问的 URL
        audio_url = SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/audio/" + new_name
        return {"message": "音频上传成功!", "音频访问路径": audio_url}

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="上传音频失败")


@api_upload.post("/video", description="上传视频文件")
async def upload_video(request : Request, current_user : User = Depends(get_current_user), file: UploadFile = File(...)):
    VIDEO_DIR = "./video"
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

     # 重命名文件
    new_name = f"{current_user.phone}_{int(time.time())}.mp4"  # 新文件名

    # 保存文件到指定目录
    file_path = await save_file(file, VIDEO_DIR, new_name)

    try:
        # 返回相对路径或可直接访问的 URL
        video_url = SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/video/" + new_name
        return {"message": "视频上传成功!", "视频访问路径": video_url}

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="上传视频失败")

async def save_file(file, directory, new_name):

    global f
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, new_name)
    print("file_path:", file_path)

    try:
        f = open(file_path, mode='wb')
        data = await file.read()
        f.write(data)
        f.close()
    finally:
        if f:
            f.close()

    return file_path