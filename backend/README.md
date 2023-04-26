
#### 🌈 介绍

基于 python + fastApi + celery + sqlalchemy + redis

- 使用软件版本
- python version 3.9.6
- mysql version 8.0.23
- redis version 6.0.9
- node version 18.15.0

#### 💒 平台地址地址
- github 
https://github.com/baizunxian/zerorunner
- gitee

#### ⛱️ 线上预览

- ZERORUNNER 自动化测试平台在线预览 <a href="https://xiaobaicodes.com:8888" target="_blank">https://xiaobaicodes.com:8888</a>


#### 🚧 项目启动初始化

```bash
# 克隆项目
git clone https://github.com/baizunxian/zerorunner.git

# 数据库脚本 将内容复制数据库执行 需要新建数据库 zerorunner
script/zerorunner.sql
# 初始化数据脚本 将内容复制数据库执行 
script/init.sql  

# 修改对应的数据库地址，redis 地址
autotest/config.py

# 安装依赖
pip install -r  requirements

# 运行项目 zerorunner/backend 目录下执行
python main.py

# 异步任务依赖 celery 启动命令

#  windows 启动，只能单线程 zerorunner/backend 目录下执行
celery -A celery_worker.worker.celery worker --pool=solo -l INFO 

# linux 启动
elery -A celery_worker.worker.celery worker --loglevel=INFO -c 10 -P solo -n zerorunner-celery-worker

# 定时任务启动
celery -A celery_worker.worker.celery beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO

# 定时任务心跳启动
celery -A celery_worker.worker.celery beat  -l INFO 

```

#### 💯 学习交流加 微信 群

- 微信群
<img src="https://github.com/baizunxian/zero_autotest_backend/blob/master/static/img/weixin.jpg?raw=true" width="220" height="220" alt="zero autotest 交流群" title="zero autotest 交流群"/>
  
#### 💌 支持作者

如果觉得框架不错，或者已经在使用了，希望你可以去 <a target="_blank" href="https://github.com/baizunxian/zero_autotest_backend">Github</a> 帮我点个 ⭐ Star，这将是对我极大的鼓励与支持, 平台会持续迭代更新。
