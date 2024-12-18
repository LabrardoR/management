from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.ai_work_group import api_ai_work_group
from app.api.upload import api_upload
from app.api.work import api_work
from app.api.user import api_user
from tortoise.contrib.fastapi import register_tortoise
from app.api.api_test import api_test
# web 服务器
import uvicorn
from typing import Generator
from app.api.user_consultation import api_consultation
from app.config import mysql_config, SERVER_PORT
from redis import StrictRedis


# 使用 lifespan 事件处理器
# 创建 FastAPI 应用并传入 lifespan 事件处理器

app = FastAPI()

app.mount('/audio', StaticFiles(directory="audio"), '音频')
app.mount('/video', StaticFiles(directory="video"), '视频')

app.include_router(api_user, prefix="/user", tags=["用户接口"])

app.include_router(api_work, prefix="/work", tags=["我的作品接口"])
app.include_router(api_upload, prefix="/upload", tags=["上传文件接口"])


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
    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, reload=True)
