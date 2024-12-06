

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import os
import ffmpeg
from tortoise.exceptions import IntegrityError

from app.models.user import User
from app.models.video import Video
from app.utils.user import get_current_user
from pathlib import Path
# 配置目录路径
AUDIO_DIR = "/var/www/html/audios"
VIDEO_DIR = "/var/www/html/videos"

api_test = APIRouter()

from fastapi import FastAPI, UploadFile, File, HTTPException
import os





@api_test.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    # 保存文件到指定目录
    file_path = save_file(file, VIDEO_DIR)

    # 获取视频时长（可以通过其他方式，如 ffmpeg 获取）
    duration = ffmpeg.probe(file_path)
    file_size = os.path.getsize(file_path)

    try:
        # 将视频文件信息保存到数据库
        video = await Video.create(
            user_id=1,
            file_name=file.filename,
            file_path=file_path,
            duration=duration,
            size=file_size
        )

        # 返回相对路径或可直接访问的 URL
        video_url = f"/videos/{file.filename}"
        return {"message": "Video uploaded successfully!", "file_path": video_url}

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error saving video information")


# 保存文件的函数
def save_file(file, directory):
    # 确保目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 使用 Path 自动适配路径分隔符
    file_path = Path(directory) / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)

