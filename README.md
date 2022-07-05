
#### 🌈 介绍

基于 python + flask + httprunner + celery + sqlalchemy + marshmallow + redis

- 使用软件版本
- python version 3.9.6
- mysql version 8.0.23
- redis version 6.0.9
- httprunner version 3.1.6
- node version 14.17.5

#### 💒 前端地址
- github 
https://github.com/baizunxian/zero_autotest_front
- gitee
https://gitee.com/xb_xiaobai/zero_autotest_front
#### 💒 后端地址
- github
  https://github.com/baizunxian/zero_autotest_backend
- gitee
  https://gitee.com/xb_xiaobai/zero_autotest_backend
#### ⛱️ 线上预览

- ZERO AUTOTEST 自动化测试平台在线预览 <a href="https://xiaobaicodes.com:8888" target="_blank">https://xiaobaicodes.com:8888</a>

- 首页
 <img src="https://github.com/baizunxian/zero_autotest_backend/blob/master/static/img/index.png?raw=true" />
 
- 报告页面
 <img src="https://github.com/baizunxian/zero_autotest_backend/blob/master/static/img/report.png?raw=true" />
  
- 自定义函数
 <img src="https://github.com/baizunxian/zero_autotest_backend/blob/master/static/img/func.png?raw=true" />



#### 🚧 项目启动初始化

```bash
# 克隆项目
git clone https://github.com/baizunxian/zero_autotest_backend

# sql 脚本执行 
script/zero_autotest.sql

# 切换到项目目录
cd zero_autotest_backend

# 修改配置 config_dev.py
# 修改对应的数据库地址，redis 地址
autotest/config_dev.py

# 安装依赖
pip install -r  requirements

# 运行项目
python manage.py runserver -p 8012

# 异步任务依赖 celery 启动命令

#  windows 启动，只能单线程
celery -A autotest.corelibs.backend.celery_worker worker --pool=solo -l INFO 

# linux 启动
elery -A autotest.corelibs.backend.celery_worker worker --loglevel=INFO -c 10 -P eventlet -n zero_worker

# 定时任务启动
celery -A autotest.corelibs.backend.celery_worker beat -S autotest.corelibs.scheduler.schedulers:DatabaseScheduler -l INFO

# 定时任务心跳启动
celery -A autotest.corelibs.backend.celery_worker beat  -l INFO 


```

#### 💯 学习交流加 微信 群

- 微信群
<img src="https://github.com/baizunxian/zero_autotest_backend/blob/master/static/img/weixin.jpg?raw=true" width="220" height="220" alt="zero autotest 交流群" title="zero autotest 交流群"/>
  
#### 💌 支持作者

如果觉得框架不错，或者已经在使用了，希望你可以去 <a target="_blank" href="https://github.com/baizunxian/zero_autotest_backend">Github</a> 帮我点个 ⭐ Star，这将是对我极大的鼓励与支持, 平台会持续迭代更新。
