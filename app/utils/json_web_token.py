import jwt
from datetime import datetime, timedelta
from typing import Dict

from app.models.user import User

SECRET_KEY = 'your_secret_key'  # 更改为更安全的密钥
ALGORITHM = 'HS256'


# 生成 JWT Token
async def create_jwt(current_user: User):
    # 设置有效期
    expiration = datetime.utcnow() + timedelta(hours=3000)  # 300小时过期
    payload = {
        "user_id": str(current_user.id),
        "phone": current_user.phone,
        "role" : current_user.role,
    }
    headers = {"alg": ALGORITHM, "typ": "JWT"}

    # 生成 token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM, headers=headers)
    print(f"Generated JWT: {token}")
    return token


# 解密 JWT Token 并验证
async def decode_jwt(token: str):
    try:
        # 解码 JWT, 并验证签名
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded JWT payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        print("Token 已过期!")
    except jwt.InvalidTokenError:
        print("Token 无效!")
