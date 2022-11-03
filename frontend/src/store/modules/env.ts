import {Module} from 'vuex';
import {EnvState, RootStateTypes} from "/@/store/interface";

const EnvModule: Module<EnvState, RootStateTypes> = {
  namespaced: true,
  state: {
    envId: null,
  },
  mutations: {
    // 设置数据字典
    setEnvId(state: any, data: any) {
      state.envId = data;
    },
  },
  actions: {
    // 设置数据字典
    async setEnvId({commit}: any, envId: number) {
      console.log(envId, "setEnvId")
      commit('setEnvId', envId);
    },
  },
};

export default EnvModule;
