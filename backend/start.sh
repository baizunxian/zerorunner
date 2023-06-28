#!/bin/sh

port=$2
if [ "$port" = "" ]; then
  port=8101
fi

if [ $1 = "app" ]; then
    echo "start app"
    /usr/local/bin/python -m gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$port
fi

if [ $1 = "celery-worker" ]; then
    echo "start celery worker"
     /usr/local/bin/python -m job -A celery_worker.worker.job worker --pool=gevent -c 10 -l INFO
fi

if [ $1 = "celery-beat" ]; then
    echo "start celery beat"
    /usr/local/bin/python  -m job -A celery_worker.worker.job beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO
fi