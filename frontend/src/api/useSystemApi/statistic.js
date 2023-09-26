import request from '/@/utils/request';

/**
 * 统计接口
 */
export function useStatisticsApi() {
  return {
    countStatistic: () => {
      return request({
        url: '/statistic/countStatistic',
        method: 'POST',
        data: {}
      });
    },
  };
}
