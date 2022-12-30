<template>
  <div class="layout-navbars-breadcrumb-user" :style="{ flex: layoutUserFlexNum }">
    <!--    <div class="layout-navbars-breadcrumb-user-icon" id="header-run-env">-->
    <!--      <el-select size="default" v-model="env_id"-->
    <!--                 placeholder="运行环境"-->
    <!--                 filterable-->
    <!--                 style="width: 100%;"-->
    <!--                 @change="setEndId"-->
    <!--      >-->
    <!--        <el-option-->
    <!--            v-for="env in envList"-->
    <!--            :key="env.id + env.name"-->
    <!--            :label="env.name"-->
    <!--            :value="env.id">-->
    <!--          <span style="float: left">{{ env.name }}</span>-->
    <!--        </el-option>-->
    <!--      </el-select>-->
    <!--    </div>-->

    <el-dropdown :show-timeout="70" :hide-timeout="50" trigger="click" @command="onComponentSizeChange">
      <div class="layout-navbars-breadcrumb-user-icon">
        <i class="iconfont icon-text_fields" title="组件大小"></i>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="large" :disabled="disabledSize === 'large'">大型</el-dropdown-item>
          <el-dropdown-item command="default" :disabled="disabledSize === 'default'">默认</el-dropdown-item>
          <el-dropdown-item command="small" :disabled="disabledSize === 'small'">小型</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <!--    <div class="layout-navbars-breadcrumb-user-icon" @click="onSearchClick">-->
    <!--      <el-icon title="菜单搜索">-->
    <!--        <ele-Search/>-->
    <!--      </el-icon>-->
    <!--    </div>-->

    <div class="layout-navbars-breadcrumb-user-icon" @click="onLayoutSetingClick">
      <i class="iconfont icon-setting" title="布局配置"></i>
    </div>
    <div class="layout-navbars-breadcrumb-user-icon">
      <el-popover placement="bottom" trigger="click" width="400px">
        <template #reference>
          <el-badge :is-dot="true">
            <el-icon title="消息">
              <ele-Bell/>
            </el-icon>
          </el-badge>
        </template>
        <UserNews/>
      </el-popover>
    </div>
    <div class="layout-navbars-breadcrumb-user-icon mr10" @click="onScreenfullClick">
      <i class="iconfont" :title="isScreenfull ? '开全屏' : '关全屏'"
         :class="!isScreenfull ? 'icon-fullscreen' : 'icon-tuichuquanping'"></i>
    </div>
    <img :src="userTextToImg(userInfo.nickname)" class="layout-navbars-breadcrumb-user-link-photo mr5"/>
    <el-dropdown :show-timeout="70" :hide-timeout="50" @command="onHandleCommandClick">
        <span class="layout-navbars-breadcrumb-user-link">
        {{ userInfo.nickname === '' ? 'common' : userInfo.nickname }}
          <el-icon class="el-icon--right">
            <ele-ArrowDown/>
          </el-icon>
        </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="/home">首页</el-dropdown-item>
          <el-dropdown-item command="backend">后端代码仓库</el-dropdown-item>
          <el-dropdown-item command="front">前端代码仓库</el-dropdown-item>
          <el-dropdown-item divided command="logOut">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <Search ref="searchRef"/>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent, getCurrentInstance, onMounted, reactive, ref, toRefs} from 'vue';
import {useRouter} from 'vue-router';
import {ElMessage, ElMessageBox} from 'element-plus';
import screenfull from 'screenfull';
import {resetRoute} from '/@/router';
import {useStore} from '/@/store';
import {Local, Session} from '/@/utils/storage';
import UserNews from '/@/layout/navBars/breadcrumb/userNews.vue';
import Search from '/@/layout/navBars/breadcrumb/search.vue';
import {useUserApi} from '/@/api/useSystemApi/user'
import {textToImg} from '/@/utils/textToImg.js'
import {useEnvApi} from "/@/api/useAutoApi/env";


export default defineComponent({
  name: 'layoutBreadcrumbUser',
  components: {UserNews, Search},
  setup() {
    const {proxy} = <any>getCurrentInstance();
    const router = useRouter();
    const store = useStore();
    const searchRef = ref();
    const state = reactive({
      isScreenfull: false,
      disabledSize: 'large',
      // environment
      env_id: null,
      envList: [],
    });
    // 获取用户信息 vuex
    const userInfo = computed(() => {
      return <any>store.state.userInfos.userInfos;
    });

    // // 设置env vuex
    // const setEndId = () => {
    //   store.dispatch("env/setEnvId", state.env_id)
    // }

    // 获取布局配置信息
    const getThemeConfig = computed(() => {
      return store.state.themeConfig.themeConfig;
    });
    // 设置分割样式
    const layoutUserFlexNum = computed(() => {
      let num: string | number = '';
      const {layout, isClassicSplitMenu} = getThemeConfig.value;
      const layoutArr: string[] = ['defaults', 'columns'];
      if (layoutArr.includes(layout) || (layout === 'classic' && !isClassicSplitMenu)) num = '1';
      else num = '';
      return num;
    });
    // 全屏点击时
    const onScreenfullClick = () => {
      if (!screenfull.isEnabled) {
        ElMessage.warning('暂不不支持全屏');
        return false;
      }
      screenfull.toggle();
      screenfull.on('change', () => {
        if (screenfull.isFullscreen) state.isScreenfull = true;
        else state.isScreenfull = false;
      });
    };
    // 布局配置 icon 点击时
    const onLayoutSetingClick = () => {
      proxy.mittBus.emit('openSetingsDrawer');
    };
    // 下拉菜单点击时
    const onHandleCommandClick = (path: string) => {
      if (path === 'logOut') {
        ElMessageBox({
          closeOnClickModal: false,
          closeOnPressEscape: false,
          title: '提示',
          message: '此操作将退出登录, 是否继续?',
          showCancelButton: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          buttonSize: 'default',
          beforeClose: (action, instance, done) => {
            if (action === 'confirm') {
              instance.confirmButtonLoading = true;
              instance.confirmButtonText = '退出中';
              useUserApi().logout()
                  .then(() => {
                    done();
                    instance.confirmButtonLoading = false;
                  })
            } else {
              done();
            }
          },
        })
            .then(async () => {
              Session.clear(); // 清除缓存/token等
              await resetRoute(); // 删除/重置路由
              ElMessage.success('安全退出成功！');
              window.location.href = ''; // 去登录页
              // setTimeout(() => {
              //   window.location.href = ''; // 去登录页
              // }, 500);
            })
            .catch(() => {
            });
      } else if (path === 'backend') {
        window.open('https://github.com/baizunxian/zero_autotest_backend');
      } else if (path === 'front') {
        window.open('https://github.com/baizunxian/zero_autotest_front');
      } else {
        router.push(path);
      }
    };
    // 菜单搜索点击
    const onSearchClick = () => {
      searchRef.value.openSearch();
    };
    // 组件大小改变
    const onComponentSizeChange = (size: string) => {
      Local.remove('themeConfig');
      getThemeConfig.value.globalComponentSize = size;
      Local.set('themeConfig', getThemeConfig.value);
      initComponentSize();
      window.location.reload();
    };
    // 初始化全局组件大小
    const initComponentSize = () => {
      switch (Local.get('themeConfig').globalComponentSize) {
        case 'large':
          state.disabledSize = 'large';
          break;
        case 'default':
          state.disabledSize = 'default';
          break;
        case 'small':
          state.disabledSize = 'small';
          break;
      }
    };

    const userTextToImg = (username: string) => {
      return textToImg(username)
    }

    // environment

    // 初始化env
    // const getEnvList = () => {
    //   useEnvApi().getList({page: 1, pageSize: 1000})
    //       .then(res => {
    //         state.envList = res.data.rows
    //       })
    // };

    // 页面加载时
    onMounted(() => {
      if (Local.get('themeConfig')) {
        initComponentSize();
      }
    });

    return {
      userInfo,
      userTextToImg,
      onLayoutSetingClick,
      onHandleCommandClick,
      onScreenfullClick,
      onSearchClick,
      onComponentSizeChange,
      searchRef,
      layoutUserFlexNum,
      ...toRefs(state),
    };
  },
});
</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb-user {
  display: flex;
  align-items: center;
  justify-content: flex-end;

  &-link {
    height: 100%;
    display: flex;
    align-items: center;
    white-space: nowrap;

    &-photo {
      width: 25px;
      height: 25px;
      border-radius: 100%;
    }
  }

  &-icon {
    padding: 0 10px;
    cursor: pointer;
    color: var(--next-bg-topBarColor);
    height: 50px;
    line-height: 50px;
    display: flex;
    align-items: center;

    &:hover {
      background: var(--next-color-user-hover);

      i {
        display: inline-block;
        animation: logoAnimation 0.3s ease-in-out;
      }
    }
  }

  ::v-deep(.el-dropdown) {
    color: var(--next-bg-topBarColor);
  }

  ::v-deep(.el-badge) {
    height: 40px;
    line-height: 40px;
    display: flex;
    align-items: center;
  }

  ::v-deep(.el-badge__content.is-fixed) {
    top: 12px;
  }
}

:deep(.el-input__inner) {
  font-family: PingFang SC, HarmonyOS_Medium, Helvetica Neue, Microsoft YaHei, sans-serif;
}
</style>
