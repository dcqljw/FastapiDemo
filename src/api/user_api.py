import json

from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from src.api.deps import TokenDeps
from src.models.user.UserModel import User, UserPydantic
from src.models.user.UserSchema import UserResponse, UserCreateSchema
from src.models.role.RoleModel import Role, UserRole
from src.models.permission.PermissionModel import Permission, RolePermission
from src.models.system.ResponseSchema import ResponseSchema

router = APIRouter(prefix="/user", tags=['user'])


@router.post("/info")
async def info(token: TokenDeps):
    user_data = await User.get_or_none(uid=token['uid']).prefetch_related("user_roles__role")
    if user_data:
        roles = [user_role.role.name for user_role in user_data.user_roles]
        user_data = await UserPydantic.from_tortoise_orm(user_data)
        user = UserResponse(**user_data.model_dump()).model_dump()
        user.update(roles=roles)
        user.update(first_login=user_data.is_first_login)
        return ResponseSchema(data=user)
    else:
        return ResponseSchema(code=2001, message="用户不存在")


@router.post("/create_user")
async def create_user(user_create: UserCreateSchema, token: TokenDeps):
    user = await User.filter(username=user_create.username)
    print(user)
    if user:
        return ResponseSchema(code=2001, message="用户已存在")
    user = await User.create(**user_create.model_dump(), email="")
    user = await UserPydantic.from_tortoise_orm(user)
    return ResponseSchema(data=UserResponse(**user.model_dump()))


@router.post("/get_user")
async def get_user(token: TokenDeps):
    user_data = await User.filter().prefetch_related("user_roles__role")
    user_list = []
    for i in user_data:
        roles = [user_role.role.name for user_role in i.user_roles]
        user_data = await UserPydantic.from_tortoise_orm(i)
        user_dump = UserResponse(**user_data.model_dump()).model_dump()
        user_dump.update(roles=roles)
        user_list.append(user_dump)
    return ResponseSchema(data=user_list)


@router.post("/delete_user")
async def delete_user(user_id: int, token: TokenDeps):
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return ResponseSchema(data={"message": "删除成功"})
    return ResponseSchema(code=2001, message="用户不存在")


@router.post("/user_add_role")
async def user_add_role():
    role = await Role.get(role_id=1)
    user = await User.get(uid=761396943799717888)
    await UserRole.create(user=user, role=role)
    return ResponseSchema(data={"message": "创建成功"})


@router.post("/get_user_role")
async def get_user_role():
    user = await User.get(uid=761396943799717888).prefetch_related("user_roles__role__role_permissions__permission")
    # for i in user.user_roles:
    #     role = i.role
    #     print(role.role_id)
    #     for j in role.role_permissions:
    #         pe = j.permission
    #         print(pe.resource)
    return ResponseSchema(data={})
