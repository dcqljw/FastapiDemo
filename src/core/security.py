from datetime import timedelta, timezone, datetime

import jwt
from passlib.context import CryptContext

from src.core.settings import settings

context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return context.hash(password)


def create_access_token(data: dict, expire_minutes: timedelta):
    expire = datetime.now(timezone.utc) + expire_minutes
    to_encode = {"exp": expire, **data}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        print(f"验证错误: {str(e)}")
        return None


if __name__ == '__main__':
    print(get_password_hash('123456'))
    token = create_access_token({"username": "admin"}, timedelta(seconds=10))
    print(token)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTM2ODk5NDEsInVpZCI6IjBlYzdkMmZmLThjMTUtNDRiZS04NDkzLTM3MTNmMTRkODI4MCIsInJvbGUiOjF9.8_RN8mXjhjes5Trgbvp2u6O4WtyEl3Gbu9NAFwLLcmI"
    print(verify_token(token))
