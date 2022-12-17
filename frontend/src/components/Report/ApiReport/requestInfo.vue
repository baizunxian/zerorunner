<template>
  <div class="request">
    <div class="request-info">
      <el-tag effect="dark" type="success">{{ request.method }}</el-tag>
      {{ request.url }}
    </div>

    <el-collapse v-model="accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <json-view v-model:data="request.body"></json-view>
      </el-collapse-item>

      <el-collapse-item name="header">
        <template #title>
          <strong>Header</strong>
        </template>
        <div v-for="(value, key) in request.headers" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>

      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, toRefs, watch} from 'vue';
import {getMethodColor} from "/@/utils/case";
import jsonView from "/@/components/jsonView/index.vue";
import * as monaco from "monaco-editor";


export default defineComponent({
  name: 'scriptController',
  components: {
    jsonView
  },
  props: {
    data: Object
  },
  setup(props) {

    const state = reactive({
      // 请求信息
      accordionName: ['body', 'header'],
      request: props.data
    });

    watch(
        () => props.data,
        () => {
          state.request = props.data
        },
        {deep: true}
    )

    onMounted(() => {
      nextTick(() => {
        state.request = props.data
      })
    })

    // 删除节点
    return {
      getMethodColor,
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>
.request-info {
  margin-bottom: 15px;
}
</style>