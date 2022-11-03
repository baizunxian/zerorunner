import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useTimedTasksApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/timedTasks/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/timedTasks/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: '/timedTasks/deleted',
        method: 'POST',
        data,
      });
    },
    taskSwitch: (data?: object) => {
      return request({
        url: '/timedTasks/taskSwitch',
        method: 'POST',
        data,
      });
    },
  };
}
