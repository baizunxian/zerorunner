import request from '/@/utils/request';

export function useUiCaseApi() {
  return {
    getList: (data) => {
      return request({
        url: '/uiCase/list',
        method: 'post',
        data,
      });
    },
    getUiCaseById: (data) => {
      return request({
        url: '/uiCase/getUiCaseById',
        method: 'post',
        data,
      });
    },
    runUiCaseById: (data) => {
      return request({
        url: '/uiCase/runUiCaseById',
        method: 'post',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/uiCase/saveOrUpdate',
        method: 'post',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/uiCase/deleted',
        method: 'post',
        data,
      });
    },
  };
}
