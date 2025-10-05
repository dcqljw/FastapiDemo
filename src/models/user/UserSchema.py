from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserLoginSchema(UserBase):
    password: str


class UserCreateSchema(UserBase):
    password: str


class UserEditPasswordSchema(UserBase):
    old_password: str
    new_password: str


class UserResponse(UserBase):
    uid: int
    email: str
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y年%m月%d日")
        }
