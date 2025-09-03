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


class UserEditPasswordSchema(UserBase):
    old_password: str
    new_password: str


class UserResponse(UserBase):
    email: str
    created_at: datetime
