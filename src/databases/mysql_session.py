import aerich
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from src.core.settings import settings

# ----------note------------
# /etc/mysql/mysql.conf.d/mysqld.cnf
# [mysqld]
# skip-name-resolve 设置这个可以提高访问速度
# 当客户端连接 MySQL 服务器时：
# 默认情况下，MySQL 会尝试通过客户端的 IP 地址进行反向 DNS 解析，获取对应的主机名
# 然后再对获取到的主机名进行正向 DNS 解析，验证是否与原始 IP 一致
# 启用 skip-name-resolve 后：
# MySQL 将完全跳过上述 DNS 解析过程
# 仅使用 IP 地址来识别客户端，不再进行主机名解析

db_config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': settings.MYSQL_HOST,
                'port': settings.MYSQL_PORT,
                'user': settings.MYSQL_USER,
                'password': settings.MYSQL_PASSWORD,
                'database': settings.MYSQL_DB,
            }
        },
    },
    'apps': {
        'models': {
            'models': ['src.models.UserModel', 'aerich.models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


@asynccontextmanager
async def register_mysql(app: FastAPI):
    try:
        async with RegisterTortoise(
                app,
                config=db_config,
                generate_schemas=True,
        ):
            yield
        await Tortoise.close_connections()
    except Exception as e:
        print(e)
