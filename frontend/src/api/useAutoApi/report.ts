import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useReportApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/report/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/report/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data?: object) => {
      return request({
        url: '/report/deleted',
        method: 'POST',
        data,
      });
    },
    getReportById: (data?: object) => {
      return request({
        url: '/report/getReportById',
        method: 'POST',
        data,
      });
    },
  };
}
