from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Header
from fastapi.exceptions import HTTPException

from src.core.security import verify_token
from src.databases.redis_session import get_redis


async def get_token(authorization: Annotated[str | None, Header()],
                    redis_client: redis.Redis = Depends(get_redis)) -> str | None:
    payload = verify_token(authorization)
    if authorization and payload:
        print(payload)
        redis_token = await redis_client.get(payload['uid'])
        if redis_token == authorization:
            return authorization
    raise HTTPException(status_code=401, detail="Invalid authorization")


TokenDeps = Annotated[str, Depends(get_token)]
