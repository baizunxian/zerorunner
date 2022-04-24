from autotest.exc.codes import (
    CODE_BAD_REQUEST,
    CODE_FORBIDDEN,
    CODE_NOT_FOUND,
    CODE_SERVER_ERROR,
    CODE_UNAUTHORIZED,
)

# 状态码与提示映射
errmsg = {
    CODE_BAD_REQUEST: '参数错误',
    CODE_UNAUTHORIZED: '权限不足',
    CODE_FORBIDDEN: '拒绝访问',
    CODE_NOT_FOUND: '无法找到资源',
    CODE_SERVER_ERROR: '服务端错误',
}
