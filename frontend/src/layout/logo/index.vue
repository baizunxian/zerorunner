<template>
  <div class="layout-logo" v-if="setShowLogo" @click="onThemeConfigChange">
    <svg-icon :name="logo" :size="400"></svg-icon>
  </div>
  <div class="layout-logo-size" v-else @click="onThemeConfigChange">
    <img :src="logoMini" class="layout-logo-size-img"/>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import {useStore} from '/@/store';
import logo from '/@/assets/logo.svg';
import logoMini from '/@/assets/logo-mini4.svg';
import SvgIcon from "/@/components/svgIcon/index.vue";

export default defineComponent({
  name: 'layoutLogo',
  components: {SvgIcon},
  setup() {
    const store = useStore();
    // 获取布局配置信息
    const getThemeConfig = computed(() => {
      return store.state.themeConfig.themeConfig;
    });
    // 设置 logo 的显示。classic 经典布局默认显示 logo
    const setShowLogo = computed(() => {
      let {isCollapse, layout} = store.state.themeConfig.themeConfig;
      return !isCollapse || layout === 'classic' || document.body.clientWidth < 1000;
    });
    // logo 点击实现菜单展开/收起
    const onThemeConfigChange = () => {
      if (store.state.themeConfig.themeConfig.layout === 'transverse') return false;
      store.state.themeConfig.themeConfig.isCollapse = !store.state.themeConfig.themeConfig.isCollapse;
    };
    return {
      logo,
      logoMini,
      setShowLogo,
      getThemeConfig,
      onThemeConfigChange,
    };
  },
});
</script>

<style scoped lang="scss">
.layout-logo {
  width: 220px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: rgb(0 21 41 / 2%) 0px 1px 4px;
  color: var(--el-color-primary);
  font-size: 16px;
  cursor: pointer;
  animation: logoAnimation 0.3s ease-in-out;

  &:hover {
    span {
      color: var(--color-primary-light-2);
    }
  }

  &-medium-img {
    width: 100%;
    margin-right: 5px;
  }
}

.layout-logo-size {
  width: 100%;
  height: 50px;
  display: flex;
  cursor: pointer;
  animation: logoAnimation 0.3s ease-in-out;

  &-img {
    width: 400px;
    height: 400px;
    margin-top: -176px;
    margin-left: -102px;
    //margin: auto;
    //position: absolute;
    //clip: rect(32px, 42px, 43px, 25px);
  }

  &:hover {
    img {
      animation: logoAnimation 0.3s ease-in-out;
    }
  }
}

.logo_title {
  display: inline-block;
  margin: 0;
  color: #fff;
  font-weight: 600;
  line-height: 50px;
  font-size: 14px;
  font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
  vertical-align: middle;
}
</style>
