mysql_config = {
        'connections': {
            'default': {
                # 'engine': tortoise.backends.asyncpg, # PostgreSQL
                'engine': 'tortoise.backends.mysql', # MySQL or Mariadb
                'credentials': {
                    'host': '115.25.46.212',
                    'port': '3306',
                    'user': 'head',
                    'password': 'headhead',
                    'database': 'manage_system',
                }
            },
        },
        'apps': {
            'models': {
                'models': ['app.models.user', 'app.models.video', 'app.models.user_form', "aerich.models"],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'time_zone': 'Asia/Shanghai'
    }


url = "https://meta.guiji.ai"
AccessKey = "69wCg6iKHMGlcULLGahXIQT3"
Secretkey = "XfYmmoZTbBOR3PPThzdpk6XKMgz8hSUMvnMBM2UtEKI9lVRfw8KLynloXo72Amjo"



# import aioredis
# from fastapi import FastAPI
#
# # 全局 Redis 连接对象
# redis = None
#
# async def init_redis():
#     global redis
#     redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True)
#
# async def close_redis():
#     global redis
#     if redis:
#         await redis.clone()

SERVER_ADDRESS = '115.25.46.212'

REDIS_PASSWORD = '932384'


REDIS_USER_REGISTER_CODE = 'user:register:code:'
REDIS_USER_LOGIN_CODE = 'user:login:code:'
REDIS_USER_RESET_CODE = 'user:reset:code:'