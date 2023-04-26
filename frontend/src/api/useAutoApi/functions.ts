import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */

const baseRoute = "/functions"

export function useFunctionsApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: `${baseRoute}/list`,
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url:  `${baseRoute}/saveOrUpdate`,
        method: 'POST',
        data
      })
    },
    getFuncInfo: (data?: object) => {
      return request({
        url: `${baseRoute}/getFuncInfo`,
        method: 'POST',
        data,
      });
    },
    deleted: (data?: object) => {
      return request({
        url: `${baseRoute}/deleted`,
        method: 'post',
        data,
      });
    },
    getFuncList: (data?: object) => {
      return request({
        url: `${baseRoute}/getFuncList`,
        method: 'post',
        data,
      });
    },
    debugFunc: (data?: object) => {
      return request({
        url: `${baseRoute}/debugFunc`,
        method: 'post',
        data,
      });
    },
  };
}
