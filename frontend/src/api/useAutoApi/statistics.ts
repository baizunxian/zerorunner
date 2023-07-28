import request from '/@/utils/request';

/**
 * 统计
 */
export function usesStatisticsApi() {
  return {
    personalStatistics: (data?: object) => {
      return request({
        url: '/statistics/personalStatistics',
        method: 'POST',
        data,
      });
    },
  };
}
