<template>
  <VariableController :data="state.variables"></VariableController>
</template>

<script setup name="ApiVariables">

import {handleEmpty} from "/@/utils/other";
import {reactive} from "vue";
import VariableController from "/@/components/Z-StepController/variable/VariableController.vue"

const state = reactive({
  variables: [],   // 变量列表
});
// 初始化数据
const setData = (data) => {
  state.variables = data ? data : []
}

// 获取表单数据
const getData = () => {
  return handleEmpty(state.variables)
}

const getDataLength = () => {
  return handleEmpty(state.variables).length
}

defineExpose({
  setData,
  getData,
  getDataLength,
})


</script>

<style lang="scss" scoped>


</style>