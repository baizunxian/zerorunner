import logging
import os

import urllib.request
from urllib.error import HTTPError
from urllib import parse


def http_request(url, timeout, headers={}):
    try:
        request = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(request, timeout=timeout)
        body = res.read().decode("utf-8")
        return res.code, body
    except HTTPError as e:
        if e.code == 304:
            logging.getLogger(__name__).warning("http_request error,code is 304, maybe you should check secret")
            return 304, None
        logging.getLogger(__name__).warning("http_request error,code is %d, msg is %s", e.code, e.msg)
        raise e


def url_encode(params):
    return parse.urlencode(params)


def makedirs_wrapper(path):
    os.makedirs(path, exist_ok=True)
