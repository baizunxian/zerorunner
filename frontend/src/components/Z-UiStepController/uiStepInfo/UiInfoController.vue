<template>
  <el-drawer
      v-model="state.openDetailPage"
      size="70%"
      append-to-body
      direction="rtl"
      destroy-on-close
      :with-header="true">
    <template #header>
      <strong>添加步骤</strong>
    </template>
    <uiInfoDetail :isView="true" :data="state.data"></uiInfoDetail>
  </el-drawer>

</template>

<script setup name="apiInfoController">
import {defineAsyncComponent, reactive} from 'vue';

const uiInfoDetail = defineAsyncComponent(() => import("./uiInfoDetail.vue"))

const state = reactive({
  openDetailPage: false,
  data: null
})

const onOpenApiInfoPage = (data) => {
  state.data = data
  state.openDetailPage = !state.openDetailPage
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