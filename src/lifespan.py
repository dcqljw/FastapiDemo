import random
import string

from src.core.security import get_password_hash, id_generator
from src.models.user.UserModel import User
from src.models.role.RoleModel import Role, UserRole
from src.models.permission.PermissionModel import Permission, RolePermission

permissions_data = [
    {"name": "用户新增", "permission_key": "user:add", "description": "用户新增"},
    {"name": "用户删除", "permission_key": "user:delete", "description": "用户删除"},
]


async def create_permission():
    role = await Role.get_or_create(name="admin", defaults={
        "description": "管理员"
    })
    for permission in permissions_data:
        permission = await Permission.get_or_create(name=permission["name"], defaults=permission)
        await RolePermission(role=role[0], permission=permission[0]).save()
    return role


async def create_admin_user():
    user = await User.get_or_none(username="admin")
    if not user:
        role = await create_permission()
        password = "".join(random.sample(string.ascii_letters + string.digits, 8))
        password = "123456"
        print("创建管理员账户")
        print(f"管理员初始账号：admin")
        print(f"管理员初始密码：{password}")
        password = get_password_hash(password)
        user = User(uid=id_generator.generate_id(), username="admin", email="", password=password, nickname="admin")
        await user.save()
        await UserRole(user=user, role=role[0]).save()
