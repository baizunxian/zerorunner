import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useReportApi() {
  return {
    getList: (data) => {
      return request({
        url: '/report/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data) {
      return request({
        url: '/report/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted: (data) => {
      return request({
        url: '/report/deleted',
        method: 'POST',
        data,
      });
    },
    getReportDetail: (data) => {
      return request({
        url: '/report/getReportDetail',
        method: 'POST',
        data,
      });
    },
    getReportStatistics: (data) => {
      return request({
        url: '/report/getReportStatistics',
        method: 'POST',
        data,
      });
    },
  };
}
