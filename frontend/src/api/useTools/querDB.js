import request from '/@/utils/request';

/**
 * 数据库查询
 */
export function useQueryDBApi() {
  return {
    // 获取数据库连接列表
    getSourceList: (data) => {
      return request({
        url: '/dataSource/sourceList',
        method: 'POST',
        data,
      });
    },
    // 获取数数据库表
    getDBList: (data) => {
      return request({
        url: '/dataSource/dbList',
        method: 'POST',
        data,
      });
    },
    // 测试连接
    testConnect: (data) => {
      return request({
        url: '/dataSource/testConnect',
        method: 'POST',
        data,
      });
    },
    // 获取数数据库表
    getTableList: (data) => {
      return request({
        url: '/dataSource/tableList',
        method: 'POST',
        data,
      });
    },
    // 获取数数据库表
    getColumnList: (data) => {
      return request({
        url: '/dataSource/columnList',
        method: 'POST',
        data,
      });
    },
    // 新增修改
    saveOrUpdate(data) {
      return request({
        url: '/dataSource/saveOrUpdateSource',
        method: 'POST',
        data
      })
    },
    deletedSource(data) {
      return request({
        url: '/dataSource/deletedSource',
        method: 'POST',
        data
      })
    },
    // 执行
    execute(data) {
      return request({
        url: '/dataSource/mysql/execute',
        method: 'POST',
        data
      })
    },
    // 执行
    showCreateTable(data) {
      return request({
        url: '/dataSource/showCreateTable',
        method: 'POST',
        data
      })
    }
  };
}
