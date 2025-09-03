from datetime import timedelta

import redis.asyncio as redis
from fastapi import APIRouter, Depends

from src.models.user.UserModel import User
from src.models.user.UserSchema import UserLoginSchema, UserEditPasswordSchema
from src.models.system.ResponseSchema import ResponseSchema
from src.core.security import verify_password, create_access_token, get_password_hash
from src.api.deps import TokenDeps
from src.databases.redis_session import get_redis

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
        form_data: UserLoginSchema,
        redis_client: redis.Redis = Depends(get_redis)
):
    data = await User.get_or_none(username=form_data.username)
    response_data = {}
    if data:
        if verify_password(form_data.password, data.password):
            token = create_access_token({"uid": data.id}, timedelta(days=10))
            response_data['token'] = token
            response_data['is_first_login'] = data.is_first_login
            await redis_client.set(data.id, token)
            return ResponseSchema(data=response_data)
    return ResponseSchema(code=4000, message="用户名或密码错误")


@router.post("/edit_password")
async def edit_password(
        form_data: UserEditPasswordSchema,
        token: TokenDeps
):
    data = await User.get_or_none(username=form_data.username)
    if data:
        if verify_password(form_data.old_password, data.password):
            data.password = get_password_hash(form_data.new_password)
            data.is_first_login = False
            await data.save()
            return ResponseSchema(data={"message": "修改成功"})
    return ResponseSchema(code=2001, message="修改失败")


@router.get("/get")
async def get(
        token: TokenDeps
):
    return token
