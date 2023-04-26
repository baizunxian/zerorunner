# -*- coding: utf-8 -*-
# @author: xiaobai

from pathlib import Path


def create_dir(file_name: str) -> Path:
    """ 创建文件夹 """
    path = Path(file_name).absolute().parent / file_name  # 拼接日志文件夹的路径
    if not Path(path).exists():  # 文件是否存在
        Path.mkdir(path)

    return path

# import os


# # 请不要随意移动该文件,创建文件夹是根据当前文件位置来创建
# def create_dir(file_name: str) -> str:
#     """ 创建文件夹 """
#     current_path = os.path.dirname(__file__)  # 获取当前文件夹

#     base_path = os.path.abspath(os.path.join(current_path, ".."))  # 获取当前文件夹的上一层文件

#     path = base_path + os.sep + file_name + os.sep  # 拼接日志文件夹的路径

#     os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建

#     return path
