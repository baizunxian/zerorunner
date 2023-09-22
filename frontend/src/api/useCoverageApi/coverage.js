import request from '/@/utils/request';

export function useCoverageReportApi() {
	return {
		getList: (data) => {
			return request({
				url: '/coverage/report/getReportList',
				method: 'post',
				data,
			});
		},

		getReportById: (data) => {
			return request({
				url: '/coverage/report/getReportById',
				method: 'post',
				data,
			});
		},

		getCoverageDetail: (data) => {
			return request({
				url: '/coverage/report/getCoverageDetail',
				method: 'post',
				data,
			});
		},
		coverageStart: (data) => {
			return request({
				url: '/coverage/report/coverageStart',
				method: 'post',
				data,
			});
		},
	};
}
