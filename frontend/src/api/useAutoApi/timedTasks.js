import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useTimedTasksApi() {
  return {
    getList: (data) => {
      return request({
        url: '/timedTasks/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data) {
      return request({
        url: '/timedTasks/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data) => {
      return request({
        url: '/timedTasks/deleted',
        method: 'POST',
        data,
      });
    },
    taskSwitch: (data) => {
      return request({
        url: '/timedTasks/taskSwitch',
        method: 'POST',
        data,
      });
    },
    checkCrontab: (data) => {
      return request({
        url: '/timedTasks/checkCrontab',
        method: 'POST',
        data,
      });
    },
    runOnceJob: (data) => {
      return request({
        url: '/timedTasks/runOnceJob',
        method: 'POST',
        data,
      });
    },
    getTaskCaseInfo: (data) => {
      return request({
        url: '/timedTasks/getTaskCaseInfo',
        method: 'POST',
        data,
      });
    },
  };
}
