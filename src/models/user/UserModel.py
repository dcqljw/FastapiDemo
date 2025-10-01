from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    uid = fields.BigIntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=255, description="用户名")
    nickname = fields.CharField(max_length=255, description="昵称")
    email = fields.CharField(max_length=255, description="邮箱")
    password = fields.CharField(max_length=255, description="密码")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    is_first_login = fields.BooleanField(default=True, description="是否首次登录")


UserPydantic = pydantic_model_creator(User, name="User")
