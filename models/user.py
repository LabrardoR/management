from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.BigIntField(pk=True,auto_increment=True, index=True)
    account = fields.CharField(max_length=256)
    username = fields.CharField(max_length=256)
    password = fields.CharField(max_length=256)
    phone = fields.CharField(max_length=128)
    avatar_url = fields.CharField(max_length=1024, description="头像地址", null=True)
    gender = fields.SmallIntField(default=0, description="0 为男，1 为女")
    email = fields.CharField(max_length=256)
    role = fields.SmallIntField(default=0, description="0 为普通用户，1 为管理员")
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    is_delete = fields.SmallIntField(default=0, description="0 为存在，1 为删除")


