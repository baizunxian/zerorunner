<template>
  <div class="content">
    <div class="block-title">环境变量</div>
    <VariableController :data="state.data.variables"></VariableController>
  </div>
</template>

<script setup name="commonConfig">

import {handleEmpty} from "/@/utils/other";
import {reactive} from "vue";
import VariableController from "/@/components/Z-StepController/variable/VariableController.vue";

const state = reactive({
  data: {
    variables: [],   // 变量列表
  },
});

// 初始化数据
const setData = (data) => {
  if (data?.variables) {
    state.data.variables = data.variables
  }
}

// 获取表单数据
const getData = () => {
  state.data.variables = handleEmpty(state.data.variables)
  return state.data
}


defineExpose({
  setData,
  getData,
})


</script>

<style lang="scss" scoped>
.block-title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 20px;
  line-height: 20px;
  background: #f7f7fc;
  color: #333333;
  border-left: 2px solid #409eff;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

</style>