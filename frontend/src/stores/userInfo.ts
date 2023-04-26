import {defineStore} from 'pinia';
import {Session} from '/@/utils/storage';
import {useUserApi} from "/@/api/useSystemApi/user";

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
  state: (): UserInfoState => ({
    userInfos: {
      id: null,
      authBtnList: [],
      avatar: '',
      roles: [],
      time: 0,
      username: '',
      nickname: '',
      user_type: null,
    },
  }),
  actions: {

    async setUserInfos() {
      if (Session.get('userInfo')) {
        this.userInfos = Session.get('userInfo');
      } else {
        this.userInfos = await this.getApiUserInfo();
        Session.set("userInfo", this.userInfos)
      }
    },

    async getApiUserInfo() {
      let {data} = await useUserApi().getUserInfoByToken()
      return data
    }
  },
});
