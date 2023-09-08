import request from '/@/utils/request';

export function useRepositoryApi() {
	return {
		getList: (data: object) => {
			return request({
				url: '/coverage/repository/getRepositoryList',
				method: 'post',
				data,
			});
		},
		getBranches: (data: object) => {
			return request({
				url: '/coverage/repository/getBranches',
				method: 'post',
				data,
			});
		},

	};
}
