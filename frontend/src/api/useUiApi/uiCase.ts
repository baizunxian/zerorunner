import request from '/@/utils/request';

export function useUiCaseApi() {
  return {
    getList: (data: object) => {
      return request({
        url: '/uiCase/list',
        method: 'post',
        data,
      });
    },
    getPageById: (data: object) => {
      return request({
        url: '/uiCase/getCaseById',
        method: 'post',
        data,
      });
    },
    saveOrUpdate: (data: object) => {
      return request({
        url: '/uiCase/saveOrUpdate',
        method: 'post',
        data,
      });
    },
    deleted: (data: object) => {
      return request({
        url: '/uiCase/deleted',
        method: 'post',
        data,
      });
    },
  };
}
