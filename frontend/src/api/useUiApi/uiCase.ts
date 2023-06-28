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
    getUiCaseById: (data: object) => {
      return request({
        url: '/uiCase/getUiCaseById',
        method: 'post',
        data,
      });
    },
    runUiCaseById: (data: object) => {
      return request({
        url: '/uiCase/runUiCaseById',
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
