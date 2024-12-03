from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.BigIntField(pk=True,auto_increment=True, index=True)
    account = fields.CharField(max_length=30)
    phone = fields.CharField(max_length=20, description="电话号/账号")
    code = fields.CharField(max_length=10, description="验证码")
    code_expire_time = fields.DatetimeField(description="验证码过期时间，五分钟")
    password = fields.CharField(max_length=30)
    gender = fields.SmallIntField(default=0, description="0 为男，1 为女")
    email = fields.CharField(max_length=30)
    role = fields.SmallIntField(default=0, description="0 为普通用户，1 为 VIP 用户，9 为管理员")
    create_time = fields.DatetimeField(auto_now_add=True)



