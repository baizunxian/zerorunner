import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useApiSuiteApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/apiSuites/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/apiSuites/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    debugSuites(data?: object) {
      return request({
        url: '/apiSuites/debugSuites',
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: '/apiSuites/deleted',
        method: 'POST',
        data,
      });
    },
    getSuitesInfo: (data?: object) => {
      return request({
        url: '/apiSuites/getSuiteInfo',
        method: 'POST',
        data,
      });
    },
  };
}
