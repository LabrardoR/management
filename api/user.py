import datetime

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

from models.user import User
from schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate

import hashlib
import random
import re

# 生成路由对象
api_user = APIRouter()

# 密码加密解密
pwd_encryption = hashlib.sha256()

@api_user.get("/code", description="生成验证码")
async def getCode(phone: str):
    # 验证手机号格式
    phone_regex = re.compile(r"^1[3-9]\d{9}$")
    if not phone_regex.match(phone):
        raise HTTPException(status_code=400, detail="手机号格式不正确！")
    # 生成随机验证码
    code = random.randint(100000, 999999)

    # 存储验证码到数据库中 -> 后期可改进为存到Redis中
    user = await User.filter(phone = phone)
    if user:
        # 更新验证码和过期时间
        user.code = str(code)
        user.code_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=5)  # 有效期5分钟
        await user.save()
    else:
        # 如果用户不存在，创建一个新用户记录
        user = await User.create(
            phone = phone,
            code = str(code),
            code_expire_time= datetime.datetime.now() + datetime.timedelta(minutes=5)
        )

    # todo 发送验证码到手机
    print(f"验证码发送到手机号 {phone}: {code}")

    return {"message": "验证码已发送！"}

@api_user.post("/register",description="用户注册")
async def register(userRegister: UserRegister, response: Response):
    phone = userRegister.phone
    code =  userRegister.code

    # 检查手机号和验证码是否为空
    if not phone or not code:
        raise HTTPException(status_code=400, detail="手机号或验证码不能为空！")

    # 查找用户
    user = await User.filter(phone = phone).first()
    # 用户存在
    if user:
        # 校验验证码
        if user.code != code:
            raise HTTPException(status_code=400, detail="验证码错误！")
        # 检查验证码是否过期
        if datetime.datetime.now() > user.code_expire_time:
            raise HTTPException(status_code=400, detail="验证码已过期！")
        # todo 用户已存在，直接登录
        # 生成 session 信息并设置 Cookie
        session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        return {"message": "登录成功", "用户ID": user.id}

    # 用户不存在，创建新用户并直接登录
    try:
        newUser = await User.create(
            phone = userRegister.phone,
            code = None,
            code_expire_time = None
        )
        # 生成 session 信息并设置 Cookie
        session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        return {"message": "注册用户成功", "user_id": newUser.id}
    except IntegrityError:
        raise HTTPException(status_code=500, detail="用户创建失败，请稍后重试")



@api_user.post("/code_login",description="验证码登录")
async def login(userLogin: UserCodeLogin, response: Response):
    phone = userLogin.phone
    code = userLogin.code
    # 校验
    if not phone or not code:
        raise HTTPException(status_code=400, detail="账号或验证码不能为空！")
    # 数据库查询

    # 查询用户
    user = await User.filter(phone = phone).filter(code = code).filter(code_expire_time__gt=datetime.datetime.now()).first()
    if user is None:
        raise HTTPException(status_code=400, detail="账号或验证码错误！")

    # 生成 session 信息并设置 Cookie
    session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)

    return {"message": "登录成功", "用户ID": user.id}

@api_user.post("/password_login",description="密码登录")
async def login(userLogin: UserPasswordLogin, response: Response):
    phone = userLogin.phone
    password = userLogin.password
    # 校验
    if not phone or not password:
        raise HTTPException(status_code=400, detail="账号或密码不能为空！")
    # 数据库查询

    # 查询用户
    user = await User.filter(phone = phone).filter(password = md5(password)).first()
    if user is None:
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    # 验证密码
    if user.password != md5(password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    # 生成 session 信息并设置 Cookie
    session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
    return {"message": "登录成功", "用户ID": user.id}

@api_user.post("/reset_password", description="（找回）重置密码")
async def reset(userReset : UserReset):
    phone = userReset.phone
    password = userReset.password
    code = userReset.code
    if not phone or not code:
        raise HTTPException(status_code=400, detail="账号或验证码不能为空！")

    user = await User.filter(phone = phone).first()
    if user is None:
        raise HTTPException(status_code=400, detail="请先注册！") ##

    if user.code != code:
        raise HTTPException(status_code=400, detail="验证码错误！")

    # 更新密码
    user = await User.filter(phone = phone).update(password = md5(password))

    return {"message": "找回密码成功", "phone" : phone}

async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 示例：根据 session_id 查找用户 -> 可按需更改为使用 Redis 或数据库
    user_id = session_id.split("_")[1]  # session_id 格式为 "session_<user_id>"
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="会话无效，请重新登录")

    return user



@api_user.get("/profile", description="获取当前用户")
async def profile(current_user: User = Depends(get_current_user)):
    current_user.password = ""
    return current_user

@api_user.post("/update", description="修改用户信息")
async def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    """
    修改用户信息接口：
    1. 普通用户只能修改自己的信息。
    2. 管理员可以修改任意用户的信息。
    3. 禁止修改不可更新的字段（id、account、create_time、update_time、is_delete）。
    """

    # 验证权限：普通用户只能修改自己的信息
    if current_user.role != 9:  # 如果当前用户不是管理员
        if update_user.phone and update_user.phone != current_user.phone:
            raise HTTPException(status_code=403, detail="没有权限修改其他用户的信息")

    # 查找目标用户
    target_user = await User.filter(account=update_user.account).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 更新字段：过滤掉禁止更新的字段
    update_fields = {"account": update_user.account}
    if update_user.username:
        update_fields["username"] = update_user.username
    if update_user.password:
        update_fields["password"] = md5(update_user.password)  # 加密存储密码
    if update_user.gender is not None:
        update_fields["gender"] = update_user.gender
    if update_user.email:
        update_fields["email"] = update_user.email

    # 更新数据库
    await User.filter(id=target_user.id).update(**update_fields)

    return {
        "message": "用户信息更新成功",
        "updated_user": update_fields
    }


@api_user.post("/logout", description="退出登录")
async def logout(response: Response):
    # 删除 Cookie
    response.delete_cookie("session_id")
    return {"message": "注销成功"}

@api_user.get("/query_all", description="查询全部用户")
async def queryAllUser(current_user: User = Depends(get_current_user)):
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="无权限！")
    user_list = await User.filter(is_delete=0).all()

    # 通过 Pydantic 模型返回精简后的字段
    return [
        UserResponse(
            id=user.id,
            account=user.account,
            phone=user.phone,
            gender=user.gender,
            email=user.email,
            role=user.role,
        )
        for user in user_list
    ]


# todo
# @api_user.delete("/delete/{user_id}", description="删除用户(逻辑删除)")
# async def update_user(user_id, current_user: User = Depends(get_current_user)):
#     # if user_id == current_user.id:
#     #     return
#     #
#     # if current_user.role != 1:
#     #     raise HTTPException(status_code=401, detail="无权限！")
#
#     return "删除用户未完成"

def md5(s):
    s = s.encode("utf8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

