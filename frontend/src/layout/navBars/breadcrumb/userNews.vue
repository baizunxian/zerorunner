<template>
  <div class="layout-navbars-breadcrumb-user-news">
    <div class="head-box">
      <div class="head-box-title">通知</div>
      <div class="head-box-btn" v-if="state.newsList.length > 0" @click="onAllReadClick">全部已读</div>
    </div>
    <div class="content-box">
      <template v-if="state.newsList.length > 0">
        <div class="content-box-item" v-for="(v, k) in state.newsList" :key="k">
          <div>{{ v.label }}</div>
          <div class="content-box-msg">
            {{ v.value }}
          </div>
          <div class="content-box-time">{{ v.time }}</div>
          <div class="content-box-img">
            <img :src="v.img" alt="">
          </div>
        </div>
      </template>
      <el-empty description="暂无通知" v-else></el-empty>
    </div>
    <div class="foot-box" @click="onGoToGitHubClick" v-if="state.newsList.length > 0">前往通知中心</div>
  </div>
</template>

<script setup lang="ts" name="layoutBreadcrumbUserNews">
import {reactive} from 'vue';
import WeixinImg from '/@/assets/weixin.png'

// 定义变量内容
const state = reactive({
  newsList: [
    {
      label: '加我微信进交流群（请备注下谢谢^_^）',
      value: '',
      img: WeixinImg,
      time: '2022-12-08',
    }
  ],
});

// 全部已读点击
const onAllReadClick = () => {
  state.newsList = [];
};
// 前往通知中心点击
const onGoToGitHubClick = () => {
  window.open('https://github.com/baizunxian/zerorunner');
};
</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb-user-news {
  .head-box {
    display: flex;
    border-bottom: 1px solid var(--el-border-color-lighter);
    box-sizing: border-box;
    color: var(--el-text-color-primary);
    justify-content: space-between;
    height: 35px;
    align-items: center;

    .head-box-btn {
      color: var(--el-color-primary);
      font-size: 13px;
      cursor: pointer;
      opacity: 0.8;

      &:hover {
        opacity: 1;
      }
    }
  }

  .content-box {
    font-size: 13px;

    .content-box-item {
      padding-top: 12px;

      &:last-of-type {
        padding-bottom: 12px;
      }

      .content-box-msg {
        color: var(--el-text-color-secondary);
        margin-top: 5px;
        margin-bottom: 5px;
      }

      .content-box-time {
        color: var(--el-text-color-secondary);
      }

      .content-box-img {
        img {
          width: 280px;
        }
      }
    }
  }

  .foot-box {
    height: 35px;
    color: var(--el-color-primary);
    font-size: 13px;
    cursor: pointer;
    opacity: 0.8;
    display: flex;
    align-items: center;
    justify-content: center;
    border-top: 1px solid var(--el-border-color-lighter);

    &:hover {
      opacity: 1;
    }
  }

  :deep(.el-empty__description p) {
    font-size: 13px;
  }
}
</style>
