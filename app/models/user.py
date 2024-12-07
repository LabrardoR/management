import uuid
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4, index=True)
    account = fields.CharField(default="", max_length=100, description="账户")
    username = fields.CharField(default="", max_length=100, description="名称")
    password = fields.CharField(default="", max_length=100, description="密码")
    phone = fields.CharField(default="", max_length=100, description="电话号")
    points = fields.IntField(default=0, description="积分")
    email = fields.CharField(default="", max_length=100)
    gender = fields.SmallIntField(default=0, description="0 为男，1 为女")
    role = fields.SmallIntField(default=0, description="0 为普通用户，1 为 VIP 用户，9 为管理员")
    create_time = fields.DatetimeField(auto_now_add=True)



