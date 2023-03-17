# -*- coding: utf-8 -*-
# @author: xiaobai


import uvicorn
from fastapi import FastAPI

from autotest.config import config
from autotest.corelibs import logger
from autotest.db import init_redis_pool
from autotest.register import register_cors, register_exception, register_middleware, register_router

app = FastAPI(description=config.PROJECT_DESC, version=config.PROJECT_VERSION)


def create_app():
    """ 注册中心 """
    # register_mount(app)  # 挂载静态文件

    register_exception(app)  # 注册捕获全局异常

    register_router(app)  # 注册路由

    register_middleware(app)  # 注册请求响应拦截

    register_cors(app)  # 初始化跨域

    logger.info("日志初始化成功！！!")  # 初始化日志


@app.on_event("startup")
async def startup():
    create_app()  # 加载注册中心
    # await init_db()  # 初始化表
    # await init_data()  # 初始化数据
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8101, reload=True)
