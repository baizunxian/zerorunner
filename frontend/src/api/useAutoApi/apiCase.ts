import request from '/@/utils/request';

const BaseApiPath = "/apiCase"
/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useApiCaseApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: `${BaseApiPath}/list`,
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: `${BaseApiPath}/saveOrUpdate`,
        method: 'POST',
        data
      })
    },
    runSuites(data?: object) {
      return request({
        url: `${BaseApiPath}/runTestCase`,
        method: 'POST',
        data
      })
    },
    debugSuites(data?: object) {
      return request({
        url: `${BaseApiPath}/debugTestCase`,
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: `${BaseApiPath}/deleted`,
        method: 'POST',
        data,
      });
    },
    getSuitesInfo: (data?: object) => {
      return request({
        url: `${BaseApiPath}/getSuiteInfo`,
        method: 'POST',
        data,
      });
    },
  };
}
