import request from '/@/utils/request';

/**
 */
export function useTaskRecordApi() {
  return {
    getTaskList: (data?: object) => {
      return request({
        url: '/job/taskList',
        method: 'post',
        data
      });
    },
  }
}
