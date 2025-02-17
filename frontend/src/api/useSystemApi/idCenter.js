import request from '/@/utils/request';

/**
 * 菜单接口
 * @method getId 获取id
 */
export function useIdCenterApi() {
  return {
    // 获取id
    getId: () => {
      return request({
        url: '/idCenter/getId',
        method: 'GET',
        data: {},
      });
    },
  }
}
