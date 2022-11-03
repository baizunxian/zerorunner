import request from '/@/utils/request';

/**
 * 用户接口
 * @method getUserList 获取用户列表
 * @method allMenu 获取菜单接口，平铺
 * @method saveOrUpdateMenu 更新保存菜单
 */
export function useFileApi() {
  return {
    upload: (data: object) => {
      return request({
        url: '/file/upload',
        method: 'POST',
        headers: {"Content-Type": "multipart/form-data"},
        data,
      });
    },
    download: (path: string) => {
      return request({
        url: '/file/download/' + path,
        method: 'GET',
      });
    },
    deleted: (data: object) => {
      return request({
        url: '/file/deleted',
        method: 'POST',
        data,
      });
    },
  };
}
