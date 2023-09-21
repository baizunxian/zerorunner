# -*- coding: utf-8 -*-
# @author: xiao bai


import asyncio
import mitmproxy.http
from mitmproxy.tools import dump
from mitmproxy import options
from loguru import logger


class InterceptRequest(object):

    def __del__(self):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        # print(flow.request)
        logger.info(flow.request)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        pass


async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)

    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(InterceptRequest())

    await master.run()
    return master


if __name__ == '__main__':
    asyncio.run(start_proxy('127.0.0.1', 8080))
