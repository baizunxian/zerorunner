# -*- coding: utf-8 -*-
# @author: xiaobai
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import config


def init_cors(app: FastAPI):
    """ 跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/ """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
