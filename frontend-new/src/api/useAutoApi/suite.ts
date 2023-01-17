import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useTestSuiteApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/testSuites/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/testSuites/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: '/testSuites/deleted',
        method: 'POST',
        data,
      });
    },
    getSuitesInfo: (data?: object) => {
      return request({
        url: '/testSuites/getSuiteInfo',
        method: 'POST',
        data,
      });
    },
  };
}
