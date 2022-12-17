<template>
  <div class="response">
    <div class="response-info">
      <el-tag type="success"
              class="response-info__item"
              effect="dark">
        {{ response.status_code === 200 ? response.status_code + ' OK' : response.status_code }}
      </el-tag>
      <el-tag type="success"
              effect="plain"
              class="response-info__item"> 响应时间：{{ stat.response_time_ms }} ms
      </el-tag>
      <el-tag effect="plain"
              class="response-info__item"> Body长度：{{ stat.content_size }}
      </el-tag>
      <el-tag type="info"
              effect="plain"
              class="response-info__item"> ContentType：{{ response.content_type }}
      </el-tag>

    </div>

    <el-collapse v-model="accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <json-view v-if="response.content_type?.indexOf('json') !== -1" v-model:data="response.body"></json-view>
        <pre v-else>{{ response.body }}</pre>
      </el-collapse-item>

      <el-collapse-item name="header">
        <template #title>
          <strong>Header</strong>
        </template>
        <div v-for="(value, key) in response.headers" :key="key">
        <span style="font-size: 12px">
          <span style="font-weight: 600">{{ key }}: </span><span>{{ value }}</span>
          </span>
        </div>
      </el-collapse-item>

      <el-collapse-item name="cookies">
        <template #title>
          <strong>Cookies</strong>
        </template>
        <div v-for="(value, key) in response.cookies" :key="key">
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
import jsonView from "/@/components/jsonView/index.vue";


export default defineComponent({
  name: 'scriptController',
  components: {jsonView},
  props: {
    data: Object,
    stat: Object,
  },

  setup(props) {
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

    return {
      ...toRefs(state)
    };
  },
});
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