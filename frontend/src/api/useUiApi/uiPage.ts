import request from '/@/utils/request';

export function useUiPageApi() {
  return {
    getList: (data: object) => {
      return request({
        url: '/uiPage/list',
        method: 'post',
        data,
      });
    },
    getPageById: (data: object) => {
      return request({
        url: '/uiPage/getPageById',
        method: 'post',
        data,
      });
    },
    saveOrUpdate: (data: object) => {
      return request({
        url: '/uiPage/saveOrUpdate',
        method: 'post',
        data,
      });
    },
    deleted: (data: object) => {
      return request({
        url: '/uiPage/deleted',
        method: 'post',
        data,
      });
    },
    getAllPageElement: (data: object) => {
      return request({
        url: '/uiPage/getAllPageElement',
        method: 'post',
        data,
      });
    },
  };
}
