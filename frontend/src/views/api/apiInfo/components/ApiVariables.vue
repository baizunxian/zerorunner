<template>
  <VariableController :data="state.variables"></VariableController>
</template>

<script lang="ts" setup name="ApiVariables">

import {handleEmpty} from "/@/utils/other";
import {reactive} from "vue";
import VariableController from "/@/components/StepController/variable/VariableController.vue"


interface baseState {
  key: string,
  value: string,
  remarks: string
}

interface variablesState {
  variables: Array<baseState>,
}

const state = reactive<variablesState>({
  variables: [],   // 变量列表
});
// 初始化数据
const setData = (data: any) => {
  state.variables = data ? data : []
}

// 获取表单数据
const getData = () => {
  return handleEmpty(state.variables)
}


defineExpose({
  setData,
  getData,
})


</script>

<style lang="scss" scoped>


</style>