import redis

from app.config import SERVER_ADDRESS, REDIS_PASSWORD


# 配置 Redis 连接
def get_redis() -> redis.StrictRedis:
    redis_conn = redis.StrictRedis(host=SERVER_ADDRESS, port=6379, db=1, password=REDIS_PASSWORD, decode_responses=True)
    return redis_conn