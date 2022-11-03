import request from '/@/utils/request';

/**
 * 数据字典
 * @method getLookupList 获取数据字典列表
 * @method saveOrUpdateLookup 更新保存数据字典
 * @method delLookup 删除数据字典
 * @method getLookupValue 获取数据字典列值
 * @method saveOrUpdateLookupValue 更新保存数据字典值
 * @method delLookupValue 删除数据字典值
 */
export function useLookupApi() {
  return {
    getAllLookup: () => {
      return request({
        url: '/lookup/getAllLookup',
        method: 'POST',
        data: {}
      });
    },
    getLookupList: (data: object) => {
      return request({
        url: '/lookup/getLookupList',
        method: 'POST',
        data,
      });
    },
    saveOrUpdateLookup: (data: object) => {
      return request({
        url: '/lookup/saveOrUpdateLookup',
        method: 'POST',
        data
      });
    },
    delLookup: (data?: object) => {
      return request({
        url: '/lookup/delLookup',
        method: 'POST',
        data,
      });
    },
    getLookupValue(data?: object) {
      return request({
        url: '/lookup/getLookupValue',
        method: 'POST',
        data
      })
    },
    saveOrUpdateLookupValue(data?: object) {
      return request({
        url: '/lookup/saveOrUpdateLookupValue',
        method: 'POST',
        data
      })
    },
    delLookupValue(data?: object) {
      return request({
        url: '/lookup/delLookupValue',
        method: 'POST',
        data
      })
    }
  };
}
