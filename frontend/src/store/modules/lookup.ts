import {Module} from 'vuex';
import {useLookupApi} from "/@/api/useSystemApi/lookup";
import {LookUpState, RootStateTypes} from "/@/store/interface";

const lookupInfoModule: Module<LookUpState, RootStateTypes> = {
  namespaced: true,
  state: {
    lookup: {},
  },
  mutations: {
    // 设置数据字典
    getLookup(state: any, data: any) {
      state.lookup = data;
    },
  },
  actions: {
    // 设置数据字典
    async setLookup({commit}: any) {
      useLookupApi().getAllLookup()
        .then((res: any) => {
          commit('getLookup', res.data);
        })
    },
  },
};

export default lookupInfoModule;
