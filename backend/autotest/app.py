import logging
import logging.config
from flask import Flask
from autotest.config import config, LOGGING_CONFIG
from autotest.config import db
from autotest.corelibs.backend import celery
from autotest.corelibs.bredis import br
from autotest.exc.middleware import init_middleware
from autotest.views import register_app


def create_app():
    """初始化app"""
    app = Flask(__name__)
    init_logging()
    register_app(app)
    init_middleware(app)
    load_configs(app)
    db.init_app(app)
    celery.init_app(app)
    br.init_app(app)
    return app


def load_configs(app: Flask):
    """加载配置"""
    for name, value in config.iteritems():
        app.config[name] = value


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
