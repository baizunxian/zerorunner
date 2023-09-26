
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
db_script/db_init.sql
# 初始化数据脚本 将内容复制数据库执行 
db_script/init.sql  

# 修改对应的数据库地址，redis 地址
autotest/config.py

# 安装依赖
pip install -r  requirements

# 运行项目 zerorunner/backend 目录下执行
python main.py

# 异步任务依赖 job 启动命令

#  windows 启动，只能单线程 zerorunner/backend 目录下执行
elery -A celery_worker.worker.job worker --pool=solo -l INFO 

# linux 启动
elery -A celery_worker.worker.job worker --loglevel=INFO -c 10 -P solo -n zerorunner-job-worker

# 定时任务启动
elery -A celery_worker.worker.job beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO

# 定时任务心跳启动
elery -A celery_worker.worker.job beat  -l INFO 

```

#### 💌 支持作者

如果觉得框架不错，或者已经在使用了，希望你可以去 <a target="_blank" href="https://github.com/baizunxian/zerorunner">Github</a> 帮我点个 ⭐ Star，这将是对我极大的鼓励与支持, 平台会持续迭代更新。
