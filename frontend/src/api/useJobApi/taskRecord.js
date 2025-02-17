import request from '/@/utils/request';

/**
 */
export function useTaskRecordApi() {
  return {
    getTaskList: (data) => {
      return request({
        url: '/job/taskList',
        method: 'post',
        data
      });
    },
  }
}
