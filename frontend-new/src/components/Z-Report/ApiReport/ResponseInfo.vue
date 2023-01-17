<template>
  <div class="response">
    <div class="response-info">
      <el-tag type="success"
              class="response-info__item"
              effect="dark">
        {{ state.response.status_code === 200 ? state.response.status_code + ' OK' : state.response.status_code }}
      </el-tag>
      <el-tag type="success"
              effect="plain"
              class="response-info__item">
        响应时间：{{ stat.response_time_ms }} ms
      </el-tag>
      <el-tag effect="plain"
              class="response-info__item">
        Body长度：{{ formatSizeUnits(stat.content_size) }}
      </el-tag>
      <el-tag type="info"
              effect="plain"
              class="response-info__item">
        ContentType：{{ state.response.content_type }}
      </el-tag>

    </div>

    <el-collapse v-model="state.accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <JsonViews v-if="state.response.content_type?.indexOf('json') !== -1"
                  v-model:data="state.response.body"></JsonViews>
        <pre v-else>{{ state.response.body }}</pre>
      </el-collapse-item>

      <el-collapse-item name="header">
        <template #title>
          <strong>Header</strong>
        </template>
        <div v-for="(value, key) in state.response.headers" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>
      </el-collapse-item>

      <el-collapse-item name="cookies">
        <template #title>
          <strong>Cookies</strong>
        </template>
        <div v-for="(value, key) in state.response.cookies" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>
      </el-collapse-item>

    </el-collapse>


  </div>
</template>

<script lang="ts" setup name="ResponseInfo">
import {nextTick, onMounted, PropType, reactive, watch} from 'vue';
import JsonViews from "/@/components/Z-JsonViews/index.vue";
import {formatSizeUnits} from "/@/utils/case"

const props = defineProps({
  data: Object as PropType<ResponseData>,
  stat: Object,
})


const state = reactive({
  // show
  accordionName: ['body', 'header', "cookies"],
  response: props.data
});

watch(
    () => props.data,
    () => {
      state.response = props.data
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    state.response = props.data
  })
})

</script>

<style lang="scss" scoped>
.response {
  .response-info {
    margin-bottom: 15px;

    .response-info__item {
      margin-right: 8px;
    }
  }
}
</style>