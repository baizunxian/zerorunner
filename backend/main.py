# -*- coding: utf-8 -*-
# @author: xiaobai

import uvicorn
from fastapi import FastAPI, Depends

from autotest.config import config
from autotest.corelibs.logger import init_logger, logger
from autotest.db.redis import init_redis_pool
from autotest.init.cors import init_cors
from autotest.init.dependencies import set_global_request
from autotest.init.exception import init_exception
from autotest.init.middleware import init_middleware
from autotest.init.mount import init_mount
from autotest.init.routers import init_router

app = FastAPI(title="zerorunner",
              description=config.PROJECT_DESC,
              version=config.PROJECT_VERSION,
              dependencies=[Depends(set_global_request)])


async def init_app():
    """ 注册中心 """
    init_mount(app)  # 挂载静态文件

    init_exception(app)  # 注册捕获全局异常

    init_router(app)  # 注册路由

    init_middleware(app)  # 注册请求响应拦截

    init_cors(app)  # 初始化跨域

    init_logger()

    logger.info("日志初始化成功！！!")  # 初始化日志


@app.on_event("startup")
async def startup():
    await init_app()  # 加载注册中心
    # from autotest.models import init_db
    # await init_db()  # 初始化表
    # await init_data()  # 初始化数据
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis


# gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8101
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8101, reload=True)
