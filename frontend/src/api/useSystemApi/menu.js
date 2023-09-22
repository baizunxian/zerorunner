import request from '/@/utils/request';

/**
 * 菜单接口
 * @method getAllMenus 获取菜单接口，路由格式
 * @method allMenu 获取菜单接口，平铺
 * @method saveOrUpdateMenu 更新保存菜单
 */
export function useMenuApi() {
  return {
    // 获取所有菜单，嵌套
    getAllMenus: () => {
      return request({
        url: '/menu/getAllMenus',
        method: 'POST',
        data: {},
      });
    },
    //后去所有菜单，平铺
    allMenu: (data) => {
      return request({
        url: '/menu/allMenu',
        method: 'POST',
        data,
      });
    },
    // 新增修改
    saveOrUpdate(data) {
      return request({
        url: '/menu/saveOrUpdate',
        method: 'POST',
        data
      })
    },
    // 删除
    deleted(data) {
      return request({
        url: '/menu/deleted',
        method: 'POST',
        data
      })
    }
  };
}
