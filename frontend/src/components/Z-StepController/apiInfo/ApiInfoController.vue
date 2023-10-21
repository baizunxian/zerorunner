<template>
  <el-drawer
      v-model="state.openApiInfoPage"
      size="70%"
      append-to-body
      direction="rtl"
      destroy-on-close
      :with-header="true">
    <template #header>
      <strong>步骤详情</strong>
    </template>
    <ApiInfo :isView="true" :api_id="state.data.source_id"></ApiInfo>
  </el-drawer>

</template>

<script setup name="apiInfoController">
import {defineAsyncComponent, reactive} from 'vue';

const ApiInfo = defineAsyncComponent(() => import("/@/views/api/apiInfo/components/EditApi.vue"))

const state = reactive({
  openApiInfoPage: false,
  data: null
})

const onOpenApiInfoPage = (data) => {
  state.data = data
  state.openApiInfoPage = !state.openApiInfoPage
}

defineExpose({
  onOpenApiInfoPage,
})
</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}
</style>