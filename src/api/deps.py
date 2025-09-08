from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Header
from fastapi.exceptions import HTTPException

from src.core.security import verify_token
from src.databases.redis_session import get_redis


async def get_token(Authorization: Annotated[str | None, Header()] = None,
                    redis_client: redis.Redis = Depends(get_redis)):
    payload = verify_token(Authorization)
    print(payload)
    if Authorization and payload:
        print(payload)
        redis_token = await redis_client.get(payload['uid'])
        print(redis_token)
        if redis_token == Authorization:
            return payload
    raise HTTPException(status_code=401, detail="登录过期,请重新登录!")


TokenDeps = Annotated[str, Depends(get_token)]
