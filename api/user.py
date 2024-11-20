from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

from models.user import User
from schemas.user import UserRegister, UserLogin, UserUpdate, UserResponse

import hashlib

# 生成路由对象
api_user = APIRouter()

# 密码加密解密
pwd_encryption = hashlib.sha256()

@api_user.post("/register",description="用户注册")
async def register(userRegister: UserRegister):
    account = userRegister.account
    password = userRegister.password
    if not account or not password:
        raise HTTPException(status_code=400, detail="账号或密码不能为空！")

    user = await User.filter(account = account).filter(is_delete = 0)
    if user:
        raise HTTPException(status_code=400, detail="该用户已存在！")
    try:
        newUser = await User.create(
            account = userRegister.account,
            username = userRegister.username,
            password = md5(userRegister.password),
            phone = userRegister.phone,
            email = userRegister.email
        )

        return {"message": "注册用户成功", "user_id": newUser.id}
    except IntegrityError:
        raise HTTPException(status_code=500, detail="用户创建失败，请稍后重试")


@api_user.post("/login",description="用户登录")
async def login(userLogin: UserLogin, response: Response):
    # 校验
    if not userLogin.account or not userLogin.password:
        raise HTTPException(status_code=400, detail="账号或密码不能为空！")
    # 数据库查询

    # 查询用户
    user = await User.filter(account=userLogin.account).filter(is_delete = 0).first()
    if user is None:
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    # 验证密码
    if user.password != md5(userLogin.password):
        raise HTTPException(status_code=400, detail="账号或密码错误！")

    # 生成 session 信息并设置 Cookie
    session_id = f"session_{user.id}"  # 可使用更复杂的生成逻辑
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)

    return {"message": "登录成功", "用户ID": user.id}

async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 示例：根据 session_id 查找用户，实际应使用 Redis 或数据库
    user_id = session_id.split("_")[1]  # 假设 session_id 格式为 "session_<user_id>"
    user = await User.filter(id=user_id).filter(is_delete=0).first()
    if not user:
        raise HTTPException(status_code=401, detail="会话无效，请重新登录")

    return user


@api_user.get("/profile", description="获取当前用户")
async def profile(current_user: User = Depends(get_current_user)):
    current_user.password = ""
    return current_user

@api_user.post("/update", description="修改用户信息")
async def update_user(update_user: UserUpdate, current_user: User = Depends(get_current_user)):
    """
    修改用户信息接口：
    1. 普通用户只能修改自己的信息。
    2. 管理员可以修改任意用户的信息。
    3. 禁止修改不可更新的字段（id、account、create_time、update_time、is_delete）。
    """

    # 验证权限：普通用户只能修改自己的信息
    if current_user.role != 1:  # 如果当前用户不是管理员
        if update_user.account and update_user.account != current_user.account:
            raise HTTPException(status_code=403, detail="您没有权限修改其他用户的信息")

    # 查找目标用户
    target_user = await User.filter(account=update_user.account).filter(is_delete = 0).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 更新字段：过滤掉禁止更新的字段
    update_fields = {"account": update_user.account}
    if update_user.username:
        update_fields["username"] = update_user.username
    if update_user.password:
        update_fields["password"] = md5(update_user.password)  # 加密存储密码
    if update_user.avatar_url:
        update_fields["avatar_url"] = update_user.avatar_url
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

@api_user.get("/queryAll", description="查询全部用户")
async def queryAllUser(current_user: User = Depends(get_current_user)):
    if current_user.role != 1:
        raise HTTPException(status_code=401, detail="无权限！")
    user_list = await User.filter(is_delete=0).all()

    # 通过 Pydantic 模型返回精简后的字段
    return [
        UserResponse(
            id=user.id,
            account=user.account,
            username=user.username,
            avatar_url=user.avatar_url,
            gender=user.gender,
            email=user.email,
            role=user.role,
        )
        for user in user_list
    ]


# todo
@api_user.delete("/delete/{user_id}", description="删除用户(逻辑删除)")
async def update_user(user_id, current_user: User = Depends(get_current_user)):
    # if user_id == current_user.id:
    #     return
    #
    # if current_user.role != 1:
    #     raise HTTPException(status_code=401, detail="无权限！")

    return "删除用户未完成"

def md5(s):
    s = s.encode("utf8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

