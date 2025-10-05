import os
import string
import random
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.databases.mysql_session import register_mysql
from src.api import auth_api, user_api
from src.lifespan import create_admin_user


@asynccontextmanager
async def init_app(app: FastAPI):
    async with register_mysql(app):
        pass
    await create_admin_user()
    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=init_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 设置static，里面存放了swagger-ui的css、js 实现离线访问
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(auth_api.router)
app.include_router(user_api.router)


@app.get("/docs", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastApiDemo API",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
