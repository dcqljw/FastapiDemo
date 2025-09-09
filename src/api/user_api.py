from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from src.api.deps import TokenDeps
from src.models.user.UserModel import User
from src.models.user.UserSchema import UserResponse
from src.models.system.ResponseSchema import ResponseSchema

router = APIRouter(prefix="/user", tags=['user'])

UserPydantic = pydantic_model_creator(User, name="User")


@router.post("/info")
async def info(token: TokenDeps):
    user_data = await User.get_or_none(id=token['uid'])
    user_data = await UserPydantic.from_tortoise_orm(user_data)
    return ResponseSchema(data=UserResponse(**user_data.model_dump()))
