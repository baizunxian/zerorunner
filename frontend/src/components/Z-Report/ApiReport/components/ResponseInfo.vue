<template>
  <div class="response">
    <div class="response-info">
      <el-tag type="success"
              class="response-info__item"
              effect="dark">
        {{ state.response?.status_code === 200 ? state.response?.status_code + ' OK' : state.response?.status_code }}
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
        ContentType：{{ state.response?.content_type }}
      </el-tag>

    </div>

    <el-collapse v-model="state.accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <z-monaco-editor
            style="height: 400px"
            v-if="state.content_type?.indexOf('json') !== -1"
            ref="monacoEditRef"
            :options="{readOnly: true}"
            v-model:value="state.body"
            lang="json"
        ></z-monaco-editor>
        <el-image
            v-else-if="state.content_type.includes('image')"
            style="width: 300px; height: 300px"
            :src="state.response?.body"
            :zoom-rate="1.2"
            :preview-src-list="[state.response?.body]"
            :initial-index="4"
            fit="cover"
        />
        <pre v-else>{{ state.response?.body }}</pre>
      </el-collapse-item>

      <el-collapse-item name="header">
        <template #title>
          <strong>Header</strong>
        </template>
        <div v-for="(value, key) in state.response?.headers" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>
      </el-collapse-item>

      <el-collapse-item name="cookies">
        <template #title>
          <strong>Cookies</strong>
        </template>
        <div v-for="(value, key) in state.response?.cookies" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>
      </el-collapse-item>

    </el-collapse>


  </div>
</template>

<script setup name="ResponseInfo">
import {nextTick, onMounted, reactive, watch} from 'vue';
import {formatSizeUnits} from "/src/utils/case"

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  stat: {
    type: Object,
    required: true
  }
})


const state = reactive({
  // show
  accordionName: ['body', 'header', "cookies"],
  response: props.data,
  body: '',
  content_type: '',
});

const initData = () => {
  state.response = props.data
  state.content_type = state.response.content_type
  state.body = state.response.body
  if (state.content_type?.indexOf('json') !== -1) {
    state.body = JSON.stringify(state.body, null, 4)
  }
}

watch(
    () => props.data,
    () => {
      nextTick(() => {
        initData()
      })
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    initData()
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