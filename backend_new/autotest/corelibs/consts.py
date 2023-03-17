# 公共
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
DEFAULT_FAIL = -1

# Cache Time
CACHE_FIVE_SECONDS = 5
CACHE_MINUTE = 60
CACHE_THREE_MINUTE = 60 * 3
CACHE_FIVE_MINUTE = 60 * 5
CACHE_TEN_MINUTE = 60 * 10
CACHE_HALF_HOUR = 60 * 30
CACHE_HOUR = 60 * 60
CACHE_THREE_HOUR = 60 * 60 * 3
CACHE_TWELVE_HOUR = 60 * 60 * 12
CACHE_DAY = 60 * 60 * 24
CACHE_WEEK = 60 * 60 * 24 * 7
CACHE_MONTH = 60 * 60 * 24 * 30

# Cache
TEST_USER_INFO = 'zero:user_token:{0}'  # 用户token缓存
TEST_EXECUTE_SET = 'zero:test_execute_set:case:{}'  # 用例执行集合
TEST_EXECUTE_STATS = 'zero:test_execute_set:stats:{}'  # 用例执行统计
TEST_EXECUTE_TASK = 'zero:test_execute_set:task:{}'  # 运行任务数
TEST_EXECUTE_PARAMETER = 'zero:test_execute_set:extract_parameter:{}'  # 变量
DATA_STRUCTURE_CASE_UPDATE = 'zero:data_structure:user:{}'  # 数据构造用户变更的接口信息
TEST_USER_LOGIN_TIME = 'zero:user_login_time:{}'  # 数据构造用户变更的接口信息

# 性能
PREFORMANCE_RUN_STATUS = 'performance_test:status'
PREFORMANCE_FREE = 0
PREFORMANCE_INIT = 10
PREFORMANCE_BUSY = 20
PREFORMANCE_ABORT = 30

PREFORMANCE_CODE = 'code'
PREFORMANCE_SIGN_CODE = 'sign_code'

THREAD_MAXMUM = 100
RUN_NUMBER_MAXMUM = 1000000
DEBUG_MAXMUM = 100
