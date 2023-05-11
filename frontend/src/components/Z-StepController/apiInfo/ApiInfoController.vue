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
    <ApiInfo :isView="true" :api_id="state.data.request.api_id"></ApiInfo>
  </el-drawer>

</template>

<script lang="ts" setup name="apiInfoController">
import {defineAsyncComponent, PropType, reactive} from 'vue';

const ApiInfo = defineAsyncComponent(() => import("/@/views/api/apiInfo/components/EditApi.vue"))

const state = reactive({
  openApiInfoPage: false,
  data: null
})

const onOpenApiInfoPage = (data: any) => {
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