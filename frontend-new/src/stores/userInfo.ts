import {defineStore} from 'pinia';
import {Session} from '/@/utils/storage';

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
  state: (): UserInfosState => ({
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
    async setUserInfos(userInfos: any) {
      if (userInfos) {
        Session.remove("userInfo")
        Session.set("userInfo", userInfos)
        console.log("userInfos", userInfos)
        this.userInfos = userInfos
      }
      // 存储用户信息到浏览器缓存
      else {
        this.userInfos = Session.get('userInfo');
      }
    },
  },
});
