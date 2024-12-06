from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.ai_work_group import api_ai_work_group
from app.api.my_digital_person import api_my_digital_person
from app.api.user import api_user
from tortoise.contrib.fastapi import register_tortoise
from app.api.api_test import api_test
# web 服务器
import uvicorn
from typing import Generator
from app.api.user_consultation import api_consultation
from app.config import mysql_config
from redis import StrictRedis



# 使用 lifespan 事件处理器

# 创建 FastAPI 应用并传入 lifespan 事件处理器

app = FastAPI()
app.include_router(api_user, prefix="/user", tags=["用户接口", ])
app.include_router(api_ai_work_group, prefix = "/ai_work_group", tags=["AI工作组接口", ])
app.include_router(api_consultation, prefix = "/form", tags=["用户咨询接口",])
app.include_router(api_test, prefix="/test", tags=["测试用的接口，后期会删除",])

# 初始化 Tortoise ORM
register_tortoise(
    app,
    config=mysql_config,
    generate_schemas=True,  # 开发环境可以生成表结构，生产环境建议关闭
    add_exception_handlers=True,  # 显示错误信息
)

@app.get("/")
async def root():
    return {"message": "FastAPI启动成功，这是接口！"}



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
