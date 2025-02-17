<template>
  <div class="login-container flex">
    <div class="login-left">
      <!--      <h1 class="text-logo">ZERORRUNER</h1>-->
      <span class="text-logo-2">{{ getThemeConfig.globalTitle }}</span>

      <div class="login-left-logo">
        <!--        <div class="login-left-logo-img">-->
        <!--        <img class="login-left-logo-img-body" :src="logoMini"/>-->
        <!--        </div>-->
        <!--        <div class="login-left-logo-text">-->
        <!--          <span>{{ getThemeConfig.globalViceTitle }}</span>-->
        <!--          <span class="login-left-logo-text-msg">{{ getThemeConfig.globalViceTitleMsg }}</span>-->
        <!--        </div>-->
      </div>
      <!--      <div class="login-left-img">-->
      <!--        <img :src="loginMain"/>-->
      <!--      </div>-->
      <!--      <img :src="loginBg" class="login-left-waves"/>-->
    </div>
    <div class="login-right flex">
      <div class="login-right-warp flex-margin">
        <span class="login-right-warp-one"></span>
        <span class="login-right-warp-two"></span>
        <div class="login-right-warp-mian">
          <div class="login-right-warp-main-title">{{ getThemeConfig.globalTitle }} 欢迎您！</div>
          <div class="login-right-warp-main-form">
            <div v-if="!state.isScan">
              <el-tabs v-model="state.tabsActiveName">
                <el-tab-pane label="账号密码登录" name="account">
                  <Account/>
                </el-tab-pane>
                <!--                <el-tab-pane label="手机号登录" name="mobile">-->
                <!--                  <Mobile/>-->
                <!--                </el-tab-pane>-->
              </el-tabs>
            </div>
            <Scan v-if="state.isScan"/>
            <!--            <div class="login-content-main-sacn" @click="state.isScan = !state.isScan">-->
            <!--              <i class="iconfont" :class="state.isScan ? 'icon-diannao1' : 'icon-barcode-qr'"></i>-->
            <!--              <div class="login-content-main-sacn-delta"></div>-->
            <!--            </div>-->
          </div>
        </div>
      </div>
    </div>

    <div class="login-footer">
      <div class="login-footer__content">
        <span style="color: #fff">ZERORUNNER</span> |
        <a style="color: #fff" href="https://beian.miit.gov.cn/" class="slide" target="_blank">粤ICP备20069344号</a>
      </div>
    </div>
  </div>
</template>

<script setup name="loginIndex">
import {computed, defineAsyncComponent, onMounted, reactive} from 'vue';
import {storeToRefs} from 'pinia';
import {useThemeConfig} from '/@/stores/themeConfig';
import {NextLoading} from '/@/utils/loading';


// 引入组件
const Account = defineAsyncComponent(() => import('/@/views/login/component/account.vue'));
const Mobile = defineAsyncComponent(() => import('/@/views/login/component/mobile.vue'));
const Scan = defineAsyncComponent(() => import('/@/views/login/component/scan.vue'));

// 定义变量内容
const storesThemeConfig = useThemeConfig();
const {themeConfig} = storeToRefs(storesThemeConfig);
const state = reactive({
  tabsActiveName: 'account',
  isScan: false,
});

// 获取布局配置信息
const getThemeConfig = computed(() => {
  return themeConfig.value;
});
// 页面加载时
onMounted(() => {
  NextLoading.done();
});
</script>

<style scoped lang="scss">
.login-container {
  height: 100%;
  //background: var(--el-color-white);
  background: url("/@/assets/bakgrounImage/bj_hc.png") no-repeat center center;
  background-size: 100% 100%;

  .login-left {
    flex: 1;
    position: relative;
    //background-color: rgba(211, 239, 255, 1);
    margin-right: 100px;

    .login-left-logo {
      display: flex;
      align-items: center;
      position: absolute;
      top: -165px;
      left: -70px;
      //top: 50px;
      //left: 80px;
      z-index: 1;
      animation: logoAnimation 0.3s ease;

      .login-left-logo-img-body {
        height: 500px;
        width: 500px;

      }

      .login-left-logo-text {
        display: flex;
        flex-direction: column;

        span {
          margin-left: 10px;
          font-size: 28px;
          color: #26a59a;
        }

        .login-left-logo-text-msg {
          font-size: 12px;
          color: #32a99e;
        }
      }
    }

    .login-left-img {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100%;
      height: 52%;

      img {
        width: 100%;
        height: 100%;
        animation: error-num 0.6s ease;
      }
    }

    .login-left-waves {
      position: absolute;
      top: 0;
      right: -100px;
    }
  }

  .login-right {
    width: 700px;

    .login-right-warp {

      //border: 1px solid var(--el-color-primary-light-3);
      border-radius: 3px;
      width: 500px;
      height: 500px;
      position: relative;
      overflow: hidden;
      //background-color: var(--el-color-white);

      backdrop-filter: blur(5px);
      border: 1px rgba(255, 255, 255, 0.4) solid;
      background-color: rgba(0, 0, 0, 0.277);
      box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px;
      border-bottom: 1px rgba(40, 40, 40, 0.35) solid;
      border-right: 1px rgba(40, 40, 40, 0.35) solid;

      .login-right-warp-one,
      .login-right-warp-two {
        position: absolute;
        display: block;
        width: inherit;
        height: inherit;

        &::before,
        &::after {
          content: '';
          position: absolute;
          z-index: 1;
        }
      }

      .login-right-warp-one {
        //&::before {
        //  filter: hue-rotate(0deg);
        //  top: 0px;
        //  left: 0;
        //  width: 100%;
        //  height: 3px;
        //  background: linear-gradient(90deg, transparent, var(--el-color-primary));
        //  animation: loginLeft 3s linear infinite;
        //}
        //
        //&::after {
        //  filter: hue-rotate(60deg);
        //  top: -100%;
        //  right: 2px;
        //  width: 3px;
        //  height: 100%;
        //  background: linear-gradient(180deg, transparent, var(--el-color-primary));
        //  animation: loginTop 3s linear infinite;
        //  animation-delay: 0.7s;
        //}
      }

      .login-right-warp-two {
        //&::before {
        //  filter: hue-rotate(120deg);
        //  bottom: 2px;
        //  right: -100%;
        //  width: 100%;
        //  height: 3px;
        //  background: linear-gradient(270deg, transparent, var(--el-color-primary));
        //  animation: loginRight 3s linear infinite;
        //  animation-delay: 1.4s;
        //}
        //
        //&::after {
        //  filter: hue-rotate(300deg);
        //  bottom: -100%;
        //  left: 0px;
        //  width: 3px;
        //  height: 100%;
        //  background: linear-gradient(360deg, transparent, var(--el-color-primary));
        //  animation: loginBottom 3s linear infinite;
        //  animation-delay: 2.1s;
        //}
      }

      .login-right-warp-mian {
        display: flex;
        flex-direction: column;
        height: 100%;

        .login-right-warp-main-title {
          height: 130px;
          line-height: 130px;
          font-size: 27px;
          text-align: center;
          letter-spacing: 3px;
          animation: logoAnimation 0.3s ease;
          animation-delay: 0.3s;
          color: #FFF;
        }

        .login-right-warp-main-form {
          flex: 1;
          padding: 0 50px 50px;

          .login-content-main-sacn {
            position: absolute;
            top: 0;
            right: 0;
            width: 50px;
            height: 50px;
            overflow: hidden;
            cursor: pointer;
            transition: all ease 0.3s;
            color: var(--el-color-primary);

            &-delta {
              position: absolute;
              width: 35px;
              height: 70px;
              z-index: 2;
              top: 2px;
              right: 21px;
              background: var(--el-color-white);
              transform: rotate(-45deg);
            }

            &:hover {
              opacity: 1;
              transition: all ease 0.3s;
              color: var(--el-color-primary) !important;
            }

            i {
              width: 47px;
              height: 50px;
              display: inline-block;
              font-size: 48px;
              position: absolute;
              right: 1px;
              top: 0px;
            }
          }
        }
      }
    }
  }
}

.login-footer {
  width: 100%;
  bottom: 30px;
  position: absolute;

  background-color: transparent;

  .login-footer__content {
    //margin: 0 auto;
    transform: translate(-50%);
    position: absolute;
    left: 50%;

    .slide {
      text-decoration: none;
    }
  }
}

.text-logo-2 {
  font-size: 40px;
  position: absolute;
  left: 50px;
  top: 50px;
  //top: 50%;
  //right: 50%;
  //transform: translate(50%, -50%);
  text-transform: uppercase;
  font-family: verdana;
  //font-size: 12em;
  font-weight: 700;
  color: #f5f5f5;
  text-shadow: 1px 1px 1px #919191,
  1px 2px 1px #919191,
  1px 3px 1px #919191,
  1px 4px 1px #919191,
  1px 5px 1px #919191,
  1px 6px 1px #919191,
  1px 7px 1px #919191,
  1px 8px 1px #919191,
  1px 9px 1px #919191,
  1px 10px 1px #919191,
  1px 18px 6px rgba(16, 16, 16, 0.4),
  1px 22px 10px rgba(16, 16, 16, 0.2),
  1px 25px 35px rgba(16, 16, 16, 0.2),
  1px 30px 60px rgba(16, 16, 16, 0.4);
}
</style>
