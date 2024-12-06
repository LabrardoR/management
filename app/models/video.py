from tortoise.models import Model
from tortoise import fields


class Video(Model):
    id = fields.BigIntField(pk=True, auto_increment=True, index=True)
    user_id = fields.BigIntField(nullable=False, index=True)
    file_name = fields.CharField(max_length=255, index=True)
    file_path = fields.CharField(max_length=255, index=True, description="文件路径")
    duration = fields.FloatField(description="视频时长（秒）")
    upload_time = fields.DatetimeField(auto_now_add=True)
