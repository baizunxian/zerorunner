import request from '/@/utils/request';

export function useUiPageApi() {
  return {
    getList: (data) => {
      return request({
        url: '/uiPage/list',
        method: 'post',
        data,
      });
    },
    getPageById: (data) => {
      return request({
        url: '/uiPage/getPageById',
        method: 'post',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/uiPage/saveOrUpdate',
        method: 'post',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/uiPage/deleted',
        method: 'post',
        data,
      });
    },
    getAllPageElement: (data) => {
      return request({
        url: '/uiPage/getAllPageElement',
        method: 'post',
        data,
      });
    },
  };
}
