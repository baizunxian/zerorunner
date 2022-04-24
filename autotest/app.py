import hashlib
import json
import logging
import logging.config
import time
import traceback

from loguru import logger
from flask import Flask, request

from autotest.config import config, LOGGING_CONFIG
from autotest.config import db
from autotest.corelibs.backend import celery
from autotest.corelibs.bredis import br
from autotest.exc import codes
from autotest.models.sys_models import RequestHistory
from autotest.views import register_app

md5 = lambda pwd: hashlib.md5(pwd.encode('utf-8')).hexdigest()


def create_app():
    """初始化app"""
    app = Flask(__name__)
    init_logging()
    register_app(app)
    # setup_after_request(app)
    load_configs(app)
    db.init_app(app)
    celery.init_app(app)
    br.init_app(app)
    return app


def load_configs(app):
    """加载配置"""
    for name, value in config.iteritems():
        app.config[name] = value


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


# def setup_after_request(app):
#     app.after_request(_request_log)


def _request_log(resp, *args, **kws):
    now = time.time()
    request_start_time = getattr(request, 'request_start_time', now)
    response = resp.get_json(silent=True)
    real_ip = request.headers.get('X-Real-Ip', request.remote_addr).split(',')[0]
    remote_addr = real_ip
    code = response.get('code') if response else codes.PARTNER_CODE_FAIL
    request_json = request.get_json(silent=True)
    user_id = request.headers.get('userId', None)
    token = request.headers.get('token', None)
    employee_code = None
    if request.endpoint in ['user.domain_login'] and request.method == 'POST':
        employee_code = request_json.get('username', None)
    if request.endpoint in ['user.cas_login'] and request.method == 'POST':
        employee_code = response.get('data', {}).get('username', None)

    # data = dict(
    #     remote_addr=remote_addr,
    #     real_ip=real_ip,
    #     request=json.dumps({'http': '{}'.format(resp.status), 'service': '{}'.format(code)}),
    #     method=request.method,
    #     url=request.url,
    #     args=json.dumps(request.args),
    #     form=json.dumps(request.form),
    #     json=json.dumps(request_json),
    #     response=None,
    #     # response=json.dumps(response),
    #     endpoint=request.endpoint,
    #     elapsed=now - request_start_time if request_start_time else None,
    #     request_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    #     user_id=user_id if user_id else None,
    #     employee_code=employee_code,
    #     env=config.Authentication,
    #     toekn=token,
    # )
    try:
        if request.method != 'OPTIONS':
            request_history = RequestHistory()
            request_history.remote_addr = remote_addr
            request_history.real_ip = real_ip
            request_history.request = json.dumps({'http': '{}'.format(resp.status), 'service': '{}'.format(code)}),
            request_history.method = request.method
            request_history.url = request.url
            request_history.args = json.dumps(request.args)
            request_history.form = json.dumps(request.form)
            request_history.json = json.dumps(request_json)
            request_history.endpoint = json.dumps(request.endpoint)
            request_history.elapsed = now - request_start_time if request_start_time else None
            request_history.request_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            request_history.user_id = user_id if user_id else None
            request_history.employee_code = employee_code
            request_history.env = config.Authentication
            request_history.token = token
            request_history.save()
    except Exception:
        logger.error(traceback.format_exc())
    return resp
