import request from '/@/utils/request';

const BaseApiPath = "/apiCase"
/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useApiCaseApi() {
  return {
    getList: (data) => {
      return request({
        url: `${BaseApiPath}/list`,
        method: 'POST',
        data,
      });
    },
    getCaseByIds: (data) => {
      return request({
        url: `${BaseApiPath}/getCaseByIds`,
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data) {
      return request({
        url: `${BaseApiPath}/saveOrUpdate`,
        method: 'POST',
        data
      })
    },
    runSuites(data) {
      return request({
        url: `${BaseApiPath}/runTestCase`,
        method: 'POST',
        data
      })
    },
    debugSuites(data) {
      return request({
        url: `${BaseApiPath}/debugTestCase`,
        method: 'POST',
        data
      })
    },
    deleted: (data) => {
      return request({
        url: `${BaseApiPath}/deleted`,
        method: 'POST',
        data,
      });
    },
    getCaseInfo: (data) => {
      return request({
        url: `${BaseApiPath}/getCaseInfo`,
        method: 'POST',
        data,
      });
    },
    getUseCaseRelation: (data) => {
      return request({
        url: `${BaseApiPath}/getUseCaseRelation`,
        method: 'POST',
        data,
      });
    },
  };
}
