from tortoise.models import Model
from tortoise import fields

class UserForm(Model):
    id = fields.BigIntField(pk=True,auto_increment=True, index=True)
    user_id = fields.BigIntField()
    phone = fields.CharField(max_length=20, null=True, description="电话号/账号")
    email = fields.CharField(max_length=30)
    message = fields.TextField()
    create_time = fields.DatetimeField(auto_now_add=True)


