<template>
  <el-drawer
      v-model="state.openApiInfoPage"
      size="70%"
      append-to-body
      direction="rtl"
      :beforeClose="handelStepData"
      destroy-on-close
      :with-header="true">
    <template #header>
      <strong>步骤详情</strong>
    </template>
    <ApiInfo ref="stepInfoRef"
             :isView="isView"
             :isDialog="true"
             :api_id="state.data.source_id"
             :stepData="state.data"></ApiInfo>
  </el-drawer>

</template>

<script setup name="apiInfoController">
import {computed, defineAsyncComponent, reactive, ref} from 'vue';

const ApiInfo = defineAsyncComponent(() => import("/@/views/api/apiInfo/components/EditApi.vue"))

const emit = defineEmits(['updateStepData'])

const state = reactive({
  openApiInfoPage: false,
  data: null
})

const stepInfoRef = ref()

const isView = computed(() => {
  return !state.data?.is_quotation
})

const onOpenStepInfoPage = (data) => {
  state.data = data
  state.openApiInfoPage = !state.openApiInfoPage
}
const handelStepData = (done) => {
  if (isView) {
    const stepData = stepInfoRef.value.getStepData()
    emit('updateStepData', stepData)
    console.log('1111', stepInfoRef.value.getStepData())
  }
  return done(false)
}

defineExpose({
  onOpenStepInfoPage,
})
</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}
</style>