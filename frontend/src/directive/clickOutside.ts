import type {App} from 'vue';
import {ClickOutside} from "element-plus";

/**
 点击外部区域触发
 */
export function clickOutside(app: App) {
  app.directive('click-outside', ClickOutside)
}
