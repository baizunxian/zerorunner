<template>
  <div class="case-tabs" style="padding: 10px">
    <el-row>
      <el-col :span="12">
        <div>
          <div class="tip">前置code</div>
          <ScriptController v-model:code-content="state.setup_code" use-type="setup"></ScriptController>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="tip">后置code</div>
        <ScriptController v-model:code-content="state.teardown_code" use-type="teardown"></ScriptController>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="apiCode">
import {reactive} from 'vue';
import ScriptController from "/@/components/Z-StepController/script/ScriptController.vue"

const state = reactive({
  setup_code: "",
  teardown_code: "",
});

// init code
const setData = (setup_code, teardown_code) => {
  state.setup_code = setup_code ? setup_code : ""
  state.teardown_code = teardown_code ? teardown_code : ""
}

// 获取code
const getData = () => {
  return {
    setup_code: state.setup_code,
    teardown_code: state.teardown_code
  }
}

const getDataLength = () => {
  return state.setup_code.length + state.teardown_code.length
}

defineExpose({
  setData,
  getData,
  getDataLength,
})

</script>

<style lang="scss" scoped>

:deep(.el-card__body) {
  padding: 8px 0 !important;
}

</style>