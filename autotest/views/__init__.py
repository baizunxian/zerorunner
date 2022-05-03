import pkgutil
import traceback
from importlib import import_module

from loguru import logger


def register_app(app):
    """
    自动注册蓝图 蓝图对象必须为bp
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
        module_info = import_module(module_name)
        if hasattr(module_info, 'bp'):
            try:
                app.register_blueprint(module_info.bp)
            except Exception as e:
                logger.error(traceback.format_exc())
