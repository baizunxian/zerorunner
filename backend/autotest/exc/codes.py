"""
正常http状态码 200 302 400 401 403 404 500

1. 当http请求失败，返回失败的http状态码
2. 当http请求验证数据失败，返回http状态码400
3. 当http请求成功，业务处理失败，返回http状态码400

当http状态码是302/400/401/403/404/500 前端这边直接处理了http请求 不往下走业务逻辑
当http状态码是200 业务状态码是自定义时 前端先处理http请求 然后处理业务逻辑 比如说表单提交 参数错误时 返回400业务状态码 前端会根据返回的错误处理逻辑 给予提示
   - 因此http状态码是200 仅仅代表网络请求正常 具体业务处理还需要根据数据包的code来判断
   - http code 200 返回数据：
        {'code': 200, message: '操作成功', 'result': {} }
   - http code 200 返回数据：
        {
            "code": 400,
            "message": "参数错误",
            "result": {
                "status": [
                    "Missing data for required field."
                ],
                "department_id": [
                    "Missing data for required field."
                ],
                "name": [
                    "Not a valid string."
                ],
                "type": [
                    "Missing data for required field."
                ]
            }
        }
"""

HTTP_OK = 200
HTTP_FOUND = 302
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500

CODE_OK = 200
CODE_FOUND = 302
CODE_BAD_REQUEST = 400
CODE_UNAUTHORIZED = 401
CODE_FORBIDDEN = 403
CODE_NOT_FOUND = 404
CODE_SERVER_ERROR = 500

# 业务状态码
PARTNER_CODE_OK = 0
PARTNER_CODE_FAIL = -1
CANNOT_DELETE_CREATED_BY_YOURSELF = -2  # 不能删除非自己创建的
CANNOT_EDIT_CREATED_BY_YOURSELF = -3  # 不能修改非自己创建的

# 100001-100100 账号体系
PARTNER_CODE_EMPLOYEE_PASSWROD_FAIL = 10001  # 账号或密码错误
PARTNER_CODE_EMPLOYEE_FAIL = 10002  # 账号错误

# 用户状态 验证  100201-100500
PARTNER_CODE_TOKEN_EXPIRED_FAIL = 10201  # token已过期

# 参数类型 300400 - 300600
PARTNER_CODE_PARAMS_FAIL = 30400  # 必填参数不能为空
WRONG_USER_NAME_OR_PASSWORD = 30401  # 用户名或者密码错误
WRONG_USER_NAME_OR_PASSWORD_LOCK = 304011  # 密码输入错误超过次数，请5分钟后再登录
WRONG_USER_NAME_OR_PASSWORD_COUNT = 304012  # 密码输入错误次数:
USERNAME_OR_EMAIL_IS_REGISTER = 30402  # 用户名或者邮箱已被注册
VERIFICATION_CODE_ERROR = 30403  # 验证码错误
USERNAME_REGISTERDE = 30412  # 用户名已被注册
EMAIL_REGISTERDE = 30413  # 邮箱已被注册
USER_ID_IS_NULL = 30406  # 用户id不能为空
PASSWORD_TWICE_IS_NOT_AGREEMENT = 30407  # 两次输入的密码不一致
OLD_PASSWORD_ERROR = 30408  # 旧密码错误
NEW_PWD_NO_OLD_PWD_EQUAL = 30409  # 新密码不能与旧密码相同
EMAIL_NOT_REGISTER = 30410  # 当前邮箱没有注册
NOT_AD_ADMINISTRATOR = 30412  # 不是管理员
DOMAIN_WRONG_USER_NAME_OR_PASSWORD = 30413  # 域用户或者密码错误

# project 项目 40000
PROJECT_HAS_MODULE_ASSOCIATION = 40000  # 项目有模块或用例关联，不能删除
PROJECT_NAME_EXIST = 40001  # 项目名以存在

# module 模块 50000
MODULE_HAS_CASE_ASSOCIATION = 50000  # 模块有用例关联
MODULE_NAME_EXIST = 50001  # 模块名以存在
MODULE_PACKAGES_EXIST = 50002  # 包已经被绑定

# case 用例/配置 60000
CASE_NAME_EXIST = 60000  # 用例名已存在，请重新命名
SUITE_NAME_EXIST = 61000  # 套件名已存在，请重新命名
CASE_NOT_EXIST = 60001  # 用例不存在
CASE_UPLOAD_FROM_POSTMAN = 60002  # 导入失败
CASE_UPLOAD_FROM_POSTMAN_JSONDecodeError = 60003  # body的json格式不正确
CASE_UPLOAD_FROM_POSTMAN_DataError = 60004  # body数据太长
CASE_UPLOAD_FROM_EXCEL_ERROR = 60005  # excel导入失败
CASE_UPLOAD_ERROR = 60006  # 文件格式不支持
# timed_tasks 70000
TASK_NAME_EXIST = 70000  # 任务名已存在，请重新命名
CRONTAB_FORMAT_ERROR = 70001  # crontab格式错误
CASE_PARAM_FAIL = 60005  # 导入文件的参数格式错误
CASE_SCENE_NUM = 60006  # 用例的场景数

# 菜单管理  70100 - 70200
MENU_HAS_MODULE_ASSOCIATION = 70100  # 菜单管理子菜单
MENU_NAME_EXIST = 70101  # 菜单名以存在

# CICD 80000
CICD_MODULE_PACDAGES_NONE = 80000  # 包名称不能为空

# 性能运行

PARAMETER_ERROR = 100405  # 参数类型错误或者为空
