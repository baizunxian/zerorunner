# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import config


def init_mount(app: FastAPI):
    """ 挂载静态文件 -- https://fastapi.tiangolo.com/zh/tutorial/static-files/ """

    # 第一个参数为url路径参数, 第二参数为静态文件目录的路径, 第三个参数是FastAPI内部使用的名字
    app.mount(f"/{config.STATIC_DIR}", StaticFiles(directory=config.STATIC_DIR), name=config.STATIC_DIR)
