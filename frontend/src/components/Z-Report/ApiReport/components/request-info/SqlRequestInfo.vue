<template>
  <div class="request">
    <el-descriptions title="SQL信息" :column="1">
      <el-descriptions-item label="数据库ip:" label-align="left" label-class-name="sql-request-label-class">{{
          data.host
        }}
      </el-descriptions-item>
      <el-descriptions-item label="端口:" label-align="left" label-class-name="sql-request-label-class">{{
          data.port
        }}
      </el-descriptions-item>
      <el-descriptions-item label="用户:" label-align="left" label-class-name="sql-request-label-class">{{
          data.user
        }}
      </el-descriptions-item>
      <el-descriptions-item label="Sql语句:" label-align="left" label-class-name="sql-request-label-class">

      </el-descriptions-item>
    </el-descriptions>

    <z-monaco-editor
        style="height: 400px"
        ref="monacoEditRef"
        :options="{readOnly: true}"
        v-model:value="data.sql"
        lang="sql"
    ></z-monaco-editor>

  </div>
</template>

<script setup>
import {computed, reactive} from 'vue';

defineOptions({name: "SqlRequestInfo"})

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

<style lang="scss">
.request-info {
  margin-bottom: 15px;
}

:deep(.sql-request-label-class) {
  width: 100px !important;
}
</style>