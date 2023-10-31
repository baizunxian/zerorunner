import request from '/@/utils/request';

/**
 * 项目使用接口
 * @method getProjectList 获取项目列表
 * @method getMenuTest 获取后端动态路由菜单(test)
 */
export function useRelationGraphApi() {
	return {
		getRelationGraph: (data) => {
			return request({
				url: '/relationGraph/getRelationGraph',
				method: 'POST',
				data,
			});
		},

	};
}
