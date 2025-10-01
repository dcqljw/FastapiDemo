from tortoise import fields, models


class Permission(models.Model):
    permission_id = fields.IntField(pk=True)
    resource = fields.CharField(max_length=255)
    action = fields.CharField(max_length=255)
    permission_key = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)


class RolePermission(models.Model):
    id = fields.IntField(pk=True)
    role = fields.ForeignKeyField("models.Role", related_name="role_permissions")
    permission = fields.ForeignKeyField("models.Permission", related_name="permissions_role")
