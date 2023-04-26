import {defineStore} from 'pinia';
import {Session} from '/@/utils/storage';
import {useUserApi} from "/@/api/useSystemApi/user";

/**
 * 用户信息
 * @methods 设置菜单信息
 */
export const useMenuInfo = defineStore('useMenuInfo', {
  state: (): MenuDataState => ({
    menuData: [],
  }),
  actions: {

    async setUserInfos() {
      if (Session.get('menuData')) {
        this.menuData = Session.get('menuData');
      } else {
        this.menuData = await this.getMenuData();
      }
    },

    async getMenuData() {
      let data: any
      if (Session.get('menuData')) {
        data = Session.get('menuData');
      } else {
        let res = await useUserApi().getMenuByToken()
        this.menuData = data = res.data

        Session.set("menuData", this.menuData)
      }
      return data

    }
  },
});
