import {ClickOutside} from "element-plus";

/**
 点击外部区域触发
 */
export function clickOutside(app) {
	app.directive('click-outside', ClickOutside)
}
