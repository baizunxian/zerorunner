import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useTestSuiteApi() {
  return {
    getList: (data) => {
      return request({
        url: '/testSuites/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data) {
      return request({
        url: '/testSuites/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data) => {
      return request({
        url: '/testSuites/deleted',
        method: 'POST',
        data,
      });
    },
    getSuitesInfo: (data) => {
      return request({
        url: '/testSuites/getSuiteInfo',
        method: 'POST',
        data,
      });
    },
  };
}
