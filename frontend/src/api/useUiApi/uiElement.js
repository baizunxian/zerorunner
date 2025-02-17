import request from '/@/utils/request';

export function useUiElementApi() {
  return {
    getList: (data) => {
      return request({
        url: '/uiElement/list',
        method: 'post',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/uiElement/saveOrUpdate',
        method: 'post',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/uiElement/deleted',
        method: 'post',
        data,
      });
    },
  };
}
