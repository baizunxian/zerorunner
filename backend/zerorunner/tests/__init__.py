# -*- coding: utf-8 -*-
# @author: xiaobai
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading


def get_print(q: Queue, t):
    while True:
        if q.empty():
            break
        a = q.get()
        print(f"thread[{t}]: {a}")
    return "OK"


def put_queue(q: Queue, i):
    q.put(i)


if __name__ == '__main__':
    q = Queue()

    for i in range(2):
        q.put(i)

    for i in range(2):
        print(q.get(timeout=1))

    # with ThreadPoolExecutor(10) as executor:
    #     future_list = []
    #     for t in range(100):
    #         future_list.append(executor.submit(put_queue, q, t))
    #     for t in range(10):
    #         future_list.append(executor.submit(get_print, q, t))
    #     future_list = [executor.submit(get_print, q, t) for t in range(10)]
    #
    # for future in as_completed(future_list):
    #     result = future.result()
    #     print(f"{threading.currentThread().getName()} get result :{result}", end='\n')
    # print(q.qsize())
    # q.join()
    #
    # print(2)
