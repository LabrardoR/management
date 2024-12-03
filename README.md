# 管理系统后端

## 启动项目
```bash
# 安装依赖
pip install -r requirements.txt
# 启动 FastAPI 项目
uvicorn main:app --reload
```

通过 http://127.0.0.1:8000/docs#/ 可以查看接口文档


# 完成的接口
- 注册
- 登录
  - 验证码登录
  - 密码登录
- 找回密码
- 查看个人信息
- 退出
- （管理员）查看全部用户信息
- 修改个人信息
- todo
- 删除用户
