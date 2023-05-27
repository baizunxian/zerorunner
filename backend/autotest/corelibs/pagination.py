# -*- coding: utf-8 -*-
# @author: xiaobai
import typing
from math import ceil

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from autotest.corelibs import g
from autotest.corelibs.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE
from autotest.db.session import provide_session
from autotest.corelibs.serialize import count_query, paginate_query, unwrap_scalars


@provide_session
async def parse_pagination(
        query: select,
        page: int = None,
        page_size: int = None,
        session: AsyncSession = None) -> typing.Dict[str, typing.Any]:
    """
    统一分页处理
    :param query: query
    :param page: query
    :param page_size: query
    :param session: session db会话
    :return:
    """
    if g.request.method == 'POST':
        request_json = await g.request.json()
        page = int(request_json.get('page', DEFAULT_PAGE)) if not page else page
        page_size = min(int(request_json.get('pageSize', DEFAULT_PER_PAGE)), 1000) if not page_size else page_size
    else:
        page = g.request.args.get('page', type=int, default=DEFAULT_PAGE) if not page else page
        page_size = min(g.request.args.get('pageSize', type=int, default=DEFAULT_PER_PAGE),
                        1000) if not page_size else page_size

    (total,) = (await session.execute(count_query(query))).scalars()
    result = (await session.execute(paginate_query(query, page=page, page_size=page_size))).fetchall()
    result = unwrap_scalars(result)
    total_page = int(ceil(float(total) / page_size))
    pagination = {
        'rowTotal': total,
        'pageSize': page_size,
        'page': page,
        'pageTotal': total_page,
        'rows': result,
    }

    return pagination
