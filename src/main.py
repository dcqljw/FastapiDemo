import os

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from src.databases.mysql_session import register_mysql
from src.core.settings import settings


@asynccontextmanager
async def init_app(app: FastAPI):
    async with register_mysql(app):
        pass
    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=init_app)

# 设置static，里面存放了swaggerui的css、js 实现离线访问
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
def index():
    return {"message": "Hello World"}


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
