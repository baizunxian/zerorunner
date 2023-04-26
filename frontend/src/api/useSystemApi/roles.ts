import request from '/@/utils/request';

/**
 * 用户接口
 * @method getUserList 获取用户列表
 * @method allMenu 获取菜单接口，平铺
 * @method saveOrUpdateMenu 更新保存菜单
 */
export function useRolesApi() {
  return {
    getList: (data?: object) => {
      return request({
        url: '/roles/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate(data?: object) {
      return request({
        url: '/roles/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    deleted(data?: object) {
      return request({
        url: '/roles/deleted',
        method: 'POST',
        data
      })
    }
  };
}
