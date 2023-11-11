<template>
  <div class="request">
    <div class="request-info">
      <el-tag effect="dark" type="success">{{ request.method }}</el-tag>
       <el-text class="mx-1 ml10" type=""> {{ request.url }}</el-text>
    </div>

    <el-collapse v-model="state.accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <JsonViews v-if="contentType.includes('json') && getBodyType() === 'object'"
                   v-model:data="request.body">
        </JsonViews>
        <div v-else-if="contentType.includes('multipart/form-data') && getBodyType() === 'object'">
          <div v-for="(value, key) in request.body" :key="key">
            <span style="font-size: 12px">
              <strong>{{ key }}: </strong><span>{{ value }}</span>
              </span>
          </div>
        </div>
        <pre v-else>{{ request.body }}</pre>
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

<script setup name="RequestInfo">
import {computed, reactive} from 'vue';
import JsonViews from "/src/components/Z-JsonViews/index.vue"

const props = defineProps({
  data: {
    type: Object,
    required: true,
  }
})

const request = computed(() => {
  return props.data
})

const state = reactive({
  // 请求信息
  accordionName: ['body', 'header'],
  request: props.data
});

const contentType = computed(() => {
  return props.data.headers['Content-Type'] || props.data.headers['content-type'] || ""
})


const getBodyType = () => {
  let body = props.data?.body
  return typeof body
}


</script>

<style lang="scss" scoped>
.request-info {
  margin-bottom: 15px;
}
</style>