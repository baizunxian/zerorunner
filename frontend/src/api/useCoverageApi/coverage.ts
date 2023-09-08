import request from '/@/utils/request';

export function useCoverageReportApi() {
	return {
		getList: (data: object) => {
			return request({
				url: '/coverage/report/getReportList',
				method: 'post',
				data,
			});
		},

		getReportById: (data: object) => {
			return request({
				url: '/coverage/report/getReportById',
				method: 'post',
				data,
			});
		},

		getCoverageDetail: (data: object) => {
			return request({
				url: '/coverage/report/getCoverageDetail',
				method: 'post',
				data,
			});
		},
		coverageStart: (data: object) => {
			return request({
				url: '/coverage/report/coverageStart',
				method: 'post',
				data,
			});
		},
	};
}
