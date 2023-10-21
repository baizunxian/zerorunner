import request from '/@/utils/request';

const BaseApiPath = "/apiInfo"
/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useApiInfoApi() {
  return {
    getList: (data) => {
      return request({
        url: `${BaseApiPath}/list`,
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
    copyApi(data) {
      return request({
        url: `${BaseApiPath}/copyApi`,
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
    runTestCase: (data) => {
      return request({
        url: `${BaseApiPath}/runTestCase`,
        method: 'POST',
        data,
      });
    },
    runApi: (data) => {
      return request({
        url: `${BaseApiPath}/runApi`,
        method: 'POST',
        data,
      });
    },
    batchRunApi: (data) => {
      return request({
        url: `${BaseApiPath}/batchRunApi`,
        method: 'POST',
        data,
      });
    },
    debugApi: (data) => {
      return request({
        url: `${BaseApiPath}/debugApi`,
        method: 'POST',
        data,
      });
    },
    getApiInfo: (data) => {
      return request({
        url: `${BaseApiPath}/getApiInfo`,
        method: 'POST',
        data,
      });
    },
    getApiInfos: (data) => {
      return request({
        url: `${BaseApiPath}/getApiInfos`,
        method: 'POST',
        data,
      });
    },
    postman2case: (data) => {
      return request({
        url: `${BaseApiPath}/postman2case`,
        method: 'POST',
        headers: {"Content-Type": "multipart/form-data"},
        data,
      });
    },
    getUseApiRelation: (data) => {
      return request({
        url: `${BaseApiPath}/getUseApiRelation`,
        method: 'POST',
        data,
      });
    },
  };
}
