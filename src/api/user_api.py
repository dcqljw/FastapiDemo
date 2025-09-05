from typing import Annotated

from fastapi import APIRouter, Header
from tortoise.contrib.pydantic import pydantic_model_creator

from src.api.deps import TokenDeps
from src.models.user.UserModel import User
from src.models.user.UserSchema import UserResponse
from src.models.system.ResponseSchema import ResponseSchema

router = APIRouter(prefix="/user", tags=['user'])

UserPydantic = pydantic_model_creator(User, name="User")


@router.post("/info")
async def info(token: TokenDeps):
    print(token)
    print(type(token))
    user_data = await User.get_or_none(id=token['uid'])
    user_data = await UserPydantic.from_tortoise_orm(user_data)
    return ResponseSchema(data=UserResponse(**user_data.model_dump()))


@router.get("/test")
async def test(authorization: Annotated[str | None, Header()] = None):
    return {"code": 200, "data": authorization}
