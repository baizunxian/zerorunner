import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useTestCaseApi() {
  return {
    getList: (data) => {
      return request({
        url: '/testcase/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data) {
      return request({
        url: '/testcase/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data) => {
      return request({
        url: '/testcase/deleted',
        method: 'POST',
        data,
      });
    },
    runTestCase: (data) => {
      return request({
        url: '/testcase/runTestCase',
        method: 'POST',
        data,
      });
    },
    runTestCaseNew: (data) => {
      return request({
        url: '/testcase/runTestCaseNew',
        method: 'POST',
        data,
      });
    },
    debugTestCase: (data) => {
      return request({
        url: '/testcase/debugTestCase',
        method: 'POST',
        data,
      });
    },
    debugTestCaseNew: (data) => {
      return request({
        url: '/testcase/debugTestCaseNew',
        method: 'POST',
        data,
      });
    },
    getTestCaseInfo: (data) => {
      return request({
        url: '/testcase/getTestCaseInfo',
        method: 'POST',
        data,
      });
    },
    postman2case: (data) => {
      return request({
        url: '/testcase/postman2case',
        method: 'POST',
        headers: {"Content-Type": "multipart/form-data"},
        data,
      });
    },
  };
}
