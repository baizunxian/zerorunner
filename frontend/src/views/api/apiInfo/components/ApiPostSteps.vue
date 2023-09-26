<template>
  <div class="step-details">
    <z-step-controller use_type="post" :steps="state.postSteps" :case_id="state.case_id"></z-step-controller>
  </div>
</template>

<script setup name="postOperation">
import {reactive} from 'vue';
import {handleEmpty} from "/@/utils/other";


const state = reactive({
  postSteps: [],
  case_id: 0,
});

//
const setData = (data, case_id) => {
  state.postSteps = []
  state.case_id = 0
  if (data) state.postSteps = data
  if (case_id) state.case_id = case_id
}

// 获取表单数据
const getData = () => {
  return handleEmpty(state.postSteps)
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

:deep(.el-card__body) {
  padding: 5px 10px;
}
</style>