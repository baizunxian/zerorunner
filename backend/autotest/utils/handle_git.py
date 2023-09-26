import asyncio
from enum import Enum

import requests

from autotest.utils.async_http import AsyncHttp
from config import config


class GiteeApiEnum(Enum):
    """gitee api枚举"""
    ALLProjects = f"{config.GITLAB_URL}/api/v5/user/repos"  # 获取所有项目
    AllBranches = f"{config.GITLAB_URL}/api/v5/repos"  # 获取所有分支


class GitlabApiEnum(Enum):
    """gitlab api枚举"""
    ALLProjects = "/api/v4/projects"  # 获取所有项目
    AllBranches = "/api/v4/projects/{id}/repository/branches"  # 获取所有分支


class HandleGit:
    access_token = "09096ebbfac7942688299f2c936ac096"

    async def set_access_token(self, access_token: str):
        """设置access_token"""
        self.access_token = access_token

    @staticmethod
    async def get_projects():
        """获取所有项目"""
        params = {
            "access_token": HandleGit.access_token,
            "visibility": "all",
            "page": 1,
            "per_page": 100
        }
        res = await AsyncHttp().request("GET", GiteeApiEnum.ALLProjects.value, params=params)

        return await res.json()

    @staticmethod
    async def get_branches():
        """获取所有分支"""
        params = {
            "access_token": HandleGit.access_token,
        }
        owner = "baizunxian"
        repo = "zero_java"
        res = await AsyncHttp().request("GET", f"{GiteeApiEnum.AllBranches.value}/{owner}/{repo}/branches",
                                        params=params)
        return res


if __name__ == '__main__':
    a = asyncio.run(HandleGit.get_projects())
    print(a)
