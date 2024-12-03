from fastapi import FastAPI
from fastapi import Request
from api.user import api_user
from api.order import api_order
from tortoise.contrib.fastapi import register_tortoise

# web 服务器
import uvicorn
import config

app = FastAPI()
app.include_router(api_user, prefix="/user", tags=["用户接口", ])


# 初始化 Tortoise ORM
register_tortoise(
    app,
    config=config.db_config,
    generate_schemas=False,  # 开发环境可以生成表结构，生产环境建议关闭
    add_exception_handlers=True,  # 显示错误信息
)

@app.get("/")
async def root():
    return {"message": "Hello 这是测试接口"}



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
