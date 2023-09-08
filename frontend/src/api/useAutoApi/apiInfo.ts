import request from '/@/utils/request';

const BaseApiPath = "/apiInfo"
/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useApiInfoApi() {
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
    deleted: (data?: object) => {
      return request({
        url: `${BaseApiPath}/deleted`,
        method: 'POST',
        data,
      });
    },
    runTestCase: (data?: object) => {
      return request({
        url: `${BaseApiPath}/runTestCase`,
        method: 'POST',
        data,
      });
    },
    runApi: (data?: object) => {
      return request({
        url: `${BaseApiPath}/runApi`,
        method: 'POST',
        data,
      });
    },
    batchRunApi: (data?: object) => {
      return request({
        url: `${BaseApiPath}/batchRunApi`,
        method: 'POST',
        data,
      });
    },
    debugApi: (data?: object) => {
      return request({
        url: `${BaseApiPath}/debugApi`,
        method: 'POST',
        data,
      });
    },
    getApiInfo: (data?: object) => {
      return request({
        url: `${BaseApiPath}/getApiInfo`,
        method: 'POST',
        data,
      });
    },
    postman2case: (data?: object) => {
      return request({
        url: `${BaseApiPath}/postman2case`,
        method: 'POST',
        headers: {"Content-Type": "multipart/form-data"},
        data,
      });
    },
  };
}
