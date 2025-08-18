from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models.UserModel import User
from src.models.UserSchema import UserSchema

bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

route = APIRouter(prefix="/auth")


@route.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await User.create(username="dcq", password="aaaa", email="dcq@qq.com")
    print(result)
    return {"message": "Login"}


@route.get("/get")
async def get(token: str = Depends(bearer)):
    return token
