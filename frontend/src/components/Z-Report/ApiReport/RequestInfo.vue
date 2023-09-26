<template>
  <div class="request">
    <div class="request-info">
      <el-tag effect="dark" type="success">{{ state.request.method }}</el-tag>
      {{ state.request.url }}
    </div>

    <el-collapse v-model="state.accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <JsonViews v-if="getBodyType() === 'object' && state.request.body !== null"
                   v-model:data="state.request.body">
        </JsonViews>
        <pre v-else>{{ state.request.body }}</pre>
      </el-collapse-item>

      <el-collapse-item name="header">
        <template #title>
          <strong>Header</strong>
        </template>
        <div v-for="(value, key) in state.request.headers" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>

      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup name="RequestInfo">
import {nextTick, onMounted, reactive, watch} from 'vue';
import JsonViews from "/@/components/Z-JsonViews/index.vue"

const props = defineProps({
  data: {
    type: Object,
    required: true,
  }
})

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

const getBodyType = () => {
  let body = props.data?.body
  return typeof body
}

onMounted(() => {
  nextTick(() => {
    state.request = props.data
  })
})

</script>

<style lang="scss" scoped>
.request-info {
  margin-bottom: 15px;
}
</style>