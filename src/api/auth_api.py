from typing import Annotated
from datetime import timedelta

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user.UserModel import User
from src.models.user.UserSchema import UserEditPasswordSchema
from src.models.system.ResponseSchema import ResponseSchema
from src.core.security import verify_password, create_access_token, get_password_hash
from src.api.deps import TokenDeps
from src.databases.redis_session import get_redis

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        redis_client: redis.Redis = Depends(get_redis)
):
    data = await User.get_or_none(username=form_data.username)
    if data:
        if verify_password(form_data.password, data.password):
            token = create_access_token({"uid": data.uid}, timedelta(days=10))
            await redis_client.set(data.uid, token)
            return {
                "access_token": token,
                "token_type": "bearer"
            }
    raise HTTPException(
        status_code=401,
        detail="检查用户名和密码",
        headers={"WWW-Authenticate": "Bearer"},
    )


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


@router.post("/logout")
async def logout(
        token: TokenDeps,
        redis_client: redis.Redis = Depends(get_redis)
):
    await redis_client.delete(token['uid'])
    return ResponseSchema(data={"message": "退出成功"})
