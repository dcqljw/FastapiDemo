from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.core.security import verify_token
from src.databases.redis_session import get_redis

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_token(token: Annotated[str | None, Depends(oauth2_schema)],
                    redis_client: redis.Redis = Depends(get_redis)):
    payload = verify_token(token)
    print(payload)
    if token and payload:
        print(payload)
        redis_token = await redis_client.get(payload['uid'])
        print(redis_token)
        if redis_token == token:
            return payload
    raise HTTPException(status_code=401, detail="登录过期,请重新登录!")


TokenDeps = Annotated[str | None, Depends(get_token)]
