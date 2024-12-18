
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from sqlalchemy.sql.functions import current_user
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
from app.models.user import User
from app.schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate
from app.utils.json_web_token import create_jwt, decode_jwt
from app.utils.redis import get_redis
from app.utils.user import get_current_user, get_code, check_code
from app.config import REDIS_USER_REGISTER_CODE, REDIS_USER_LOGIN_CODE, REDIS_USER_RESET_CODE
import hashlib

# 生成路由对象
api_user = APIRouter()

redis = get_redis()
# 密码加密解密
pwd_encryption = hashlib.sha256()

@api_user.get("/register_code", description="发送注册账号的验证码")
async def register_code(phone : str):
    return await get_code(phone, REDIS_USER_REGISTER_CODE)

@api_user.get("/login_code", description="发送登录账号的验证码")
async def login_code(phone : str):
    return await get_code(phone, REDIS_USER_LOGIN_CODE)

@api_user.get("/reset_code", description="发送找回（重置）密码的验证码")
async def reset_code(phone : str):
    return await get_code(phone, REDIS_USER_RESET_CODE)



@api_user.post("/register",description="用户注册")
async def register(user_register: UserRegister, response: Response):
    username = user_register.username
    phone = user_register.phone
    password = user_register.password
    code =  user_register.code

    # 检查信息是否为空
    if not phone:
        raise HTTPException(status_code=400, detail="手机号不得为空！")
    if not code:
        raise HTTPException(status_code=400, detail="验证码不得为空！")
    if not password:
        raise HTTPException(status_code=400, detail="密码不得为空！")
    if not username:
        username = "用户" + str(phone)

    # 校验验证码
    await check_code(code, phone, REDIS_USER_REGISTER_CODE)
    # 查找用户
    user = await User.filter(phone = phone).first()
    # 用户存在
    if user:

        # 生成 session 信息并设置 Cookie
        session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        return {"message": "用户已存在，已登录", "用户ID": user.id}
    else:
        # 用户不存在，创建新用户并直接登录
        try:
            newUser = await User.create(
                phone = phone,
                username = username,
                password = md5(password)
            )
            # 生成 session 信息并设置 Cookie
            session_id = f"session_{newUser.id}"  # 可使用更复杂的生成逻辑
            response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
            return {"message": "注册用户成功", "user_id": newUser.id}
        except IntegrityError:
            raise HTTPException(status_code=500, detail="用户创建失败，请稍后重试")

@api_user.post("/code_login",description="手机号验证码登录")
async def login(user_login: UserCodeLogin, response: Response):
    phone = user_login.phone
    code = user_login.code
    # 校验
    if not phone or not code:
        raise HTTPException(status_code=400, detail="手机号或验证码不能为空！")
    # 数据库查询

    # 查询用户
    user = await User.filter(phone = phone).first()
    if user is None:
        raise HTTPException(status_code=400, detail="用户不存在！")
    await check_code(code, phone, REDIS_USER_LOGIN_CODE)

    # 生成 session 信息并设置 Cookie
    session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)

    return {"message": "登录成功", "用户ID": user.id}

@api_user.post("/password_login",description="密码登录（输入手机号和账号均可）")
async def login(user_login: UserPasswordLogin, response: Response):
    account = user_login.account # 可能为账号，可能为手机号
    password = user_login.password
    # 校验
    if not account or not password:
        raise HTTPException(status_code=400, detail="账号或密码不能为空！")
    # 数据库查询
    # 数据库查询，使用 Q 进行联合查询（账号或手机号）
    user = await User.filter(Q(account=account) | Q(phone=account)).first()
    if user is None:
        raise HTTPException(status_code=400, detail="用户不存在！")

    # 验证密码
    if user.password != md5(password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    token = await create_jwt(user)

    return {"message": "登录成功", "token": token}

@api_user.post("/reset_password", description="手机号找回（重置）密码")
async def reset(user_reset : UserReset):
    phone = user_reset.phone
    password = user_reset.password
    code = user_reset.code
    if not phone:
        raise HTTPException(status_code=400, detail="手机号不能为空！")
    if not password:
        raise HTTPException(status_code=400, detail="密码不能为空！")
    if not code:
        raise HTTPException(status_code=400, detail="验证码不能为空！")

    user = await User.filter(phone = phone).first()
    if user is None:
        raise HTTPException(status_code=400, detail="账号不存在，请先注册！") #
    await check_code(code, phone, REDIS_USER_RESET_CODE)
    # 更新密码
    user = await User.filter(phone = phone).update(password = md5(password))

    return {"message": "找回密码成功", "phone" : phone}


@api_user.get("/profile/{token}", description="获取当前用户")
async def profile(token : str):
    data = await decode_jwt(token)
    return data

@api_user.post("/update/{token}", description="修改用户信息")
async def update_user(token : str, user_update: UserUpdate):
    """
    修改用户信息接口：
    1. 普通用户只能修改自己的信息。
    2. 管理员可以修改任意用户的信息。
    3. 禁止修改不可更新的字段
    UserUpdate 字段
    id: Optional[str] 禁止修改
    username: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[int] = None
    email: Optional[str] = None
    """
    data = await decode_jwt(token)

    username = user_update.username
    phone = user_update.phone
    password = user_update.password
    gender = user_update.gender
    email = user_update.email

    if user_update.id is None:
        raise HTTPException(status_code=400, detail="信息有误")


    # 验证权限：普通用户只能修改自己的信息
    if data.role != 9:  # 如果当前用户不是管理员
        if user_update.id != data.id:
            raise HTTPException(status_code=403, detail="没有权限修改其他用户的信息")

    # 查找原用户
    original_user = await User.filter(id=user_update.id).first()
    if not original_user:
        raise HTTPException(status_code=404, detail="用户不存在，操作非法")

    if username is None:
        username = original_user.username
    if phone is None:
        phone = original_user.phone
    if password is None:
        password = original_user.password
    if gender is None:
        gender = original_user.gender
    if email is None:
        email = original_user.email

    # 更新数据库
    await User.filter(id = user_update.id).update(phone = user_update.phone, username = username, password = md5(user_update.password), gender = user_update.gender, email = user_update.email)
    updated_user = await User.filter(id = user_update.id).update(phone = user_update.phone)
    return {
        "message": "用户信息更新成功！",
        "user": updated_user
    }

@api_user.post("/logout", description="退出登录")
async def logout(response: Response):
    # 删除 Cookie
    response.delete_cookie("session_id")
    return {"message": "注销成功"}

# @api_user.get("/query_all", description="查询全部用户")
# async def query_all_user():
#     if current_user.role != 9:
#         raise HTTPException(status_code=403, detail="无管理员权限！")
#     user_list = await User.filter().all()
#
#     # 通过 Pydantic 模型返回精简后的字段
#     return [
#         UserResponse(
#             id=user.id,
#             account=user.account,
#             username = user.username,
#             password = "",
#             phone=user.phone,
#             points=user.points,
#             gender=user.gender,
#             email=user.email,
#             role=user.role,
#         )
#         for user in user_list
#     ]

# @api_user.get("/get_video_list")
# async def get_video_list():
#
#     return

def md5(s):
    s = s.encode("utf8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

