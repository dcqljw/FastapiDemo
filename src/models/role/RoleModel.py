from tortoise import fields, models


class Role(models.Model):
    role_id = fields.IntField(pk=True, description="角色ID")
    name = fields.CharField(max_length=255, description="角色名称")
    description = fields.CharField(max_length=255, description="角色描述")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")


class UserRole(models.Model):
    id = fields.IntField(pk=True, description="用户角色ID")
    user = fields.ForeignKeyField("models.User", related_name="user_roles", description="用户ID")
    role = fields.ForeignKeyField("models.Role", related_name="role_users", description="角色ID")

    class Meta:
        table = "user_role"
