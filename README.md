
#### 🌈 介绍

基于 python + flask + httprunner3.1.6 + celery + sqlalchemy + marshmallow + redis

#### ⛱️ 线上预览

- ZERO AUTOTEST 自动化测试平台在线预览 <a href="https://xiaobaicodes.com:8888" target="_blank">https://xiaobaicodes.com:8888</a>

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
<img src="https://img.xiaobaicodes.com/img/system/1650545572624/image-1650545500539-U25pcGFzdGVfMjAyMi0wNC0yMV8yMC01MS0yNC5wbmc=.png" alt="zero autotest 交流群" title="zero autotest 交流群"/>


#### 💒 前端地址

- <a target="_blank" href="https://github.com/baizunxian/zero_autotest_front">zero_autotest_front</a>

#### 💌 支持作者

如果觉得框架不错，或者已经在使用了，希望你可以去 <a target="_blank" href="https://github.com/baizunxian/zero_autotest_backend">Github</a> 帮我点个 ⭐ Star，这将是对我极大的鼓励与支持, 平台会持续迭代更新。
