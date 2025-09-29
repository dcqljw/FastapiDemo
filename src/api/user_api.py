from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from src.api.deps import TokenDeps
from src.models.user.UserModel import User
from src.models.user.UserSchema import UserResponse, UserCreateSchema
from src.models.role.RoleModel import Role
from src.models.system.ResponseSchema import ResponseSchema

router = APIRouter(prefix="/user", tags=['user'])

UserPydantic = pydantic_model_creator(User, name="User")


@router.post("/info")
async def info(token: TokenDeps):
    user_data = await User.get_or_none(id=token['uid'])
    user_data = await UserPydantic.from_tortoise_orm(user_data)
    return ResponseSchema(data=UserResponse(**user_data.model_dump()))


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
    user_data = await User.filter()
    user_list = []
    for i in user_data:
        user_data = await UserPydantic.from_tortoise_orm(i)
        user_list.append(UserResponse(**user_data.model_dump()))
    return ResponseSchema(data=user_list)


@router.post("/delete_user")
async def delete_user(user_id: int, token: TokenDeps):
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return ResponseSchema(data={"message": "删除成功"})
    return ResponseSchema(code=2001, message="用户不存在")


@router.post("/test")
async def test():
    role = await Role.create(name="admin", description="管理员")
    user = await User.create(username="test1", password="test", email="")
    role.users = user
    return ResponseSchema(data={"message": "创建成功"})


@router.post("/testget")
async def testget():
    user = await User.get_or_none(username="admin").prefetch_related("role")
    role = user.role.name
    user = await UserPydantic.from_tortoise_orm(user)
    return ResponseSchema(data=UserResponse(**user.model_dump(), role=role))
