from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.my_voice import api_my_voice
from app.api.upload import api_upload
from app.api.work import api_work
from app.api.user import api_user
from tortoise.contrib.fastapi import register_tortoise
# web 服务器
import uvicorn
from app.config import mysql_config, SERVER_PORT
import os
from fastapi.middleware.cors import CORSMiddleware

# 使用 lifespan 事件处理器
# 创建 FastAPI 应用并传入 lifespan 事件处理器

app = FastAPI()




# 确保音频和视频目录存在
if not os.path.exists("audio"):
    os.makedirs("audio")
if not os.path.exists("video"):
    os.makedirs("video")

app.mount('/audio', StaticFiles(directory="audio"), '音频')
app.mount('/video', StaticFiles(directory="video"), '视频')

app.include_router(api_user, prefix="/user", tags=["用户接口"])

app.include_router(api_work, prefix="/work", tags=["我的作品接口"])
app.include_router(api_upload, prefix="/upload", tags=["上传文件接口"])
app.include_router(api_my_voice,prefix="/my_voice",tags=["我的声音接口"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 初始化 Tortoise ORM
register_tortoise(
    app,
    config=mysql_config,
    generate_schemas=False,  # 开发环境可以生成表结构，生产环境建议关闭
    add_exception_handlers=True,  # 显示错误信息
)

@app.get("/")
async def root():
    return {"message": "FastAPI启动成功，这是接口！"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=SERVER_PORT, reload=True)
