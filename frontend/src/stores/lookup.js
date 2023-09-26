import {defineStore} from 'pinia';
import {useLookupApi} from "/@/api/useSystemApi/lookup"

/**
 * 路由列表
 * @methods setLookup 设置数据字典
 * @methods setColumnsMenuHover 设置分栏布局菜单鼠标移入 boolean
 * @methods setColumnsNavHover 设置分栏布局最左侧导航鼠标移入 boolean
 */
export const useLookup = defineStore('lookupList', {
	state: () => ({
		lookupList: []
	}),
	actions: {
		async setLookup() {
			let res = await useLookupApi().getAllLookup()
			this.lookupList = res.data;
		},
	},
});
