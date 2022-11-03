<template>
  <div class="step-details">
    <step-controller step_type="pre" :data="teardown_hooks" :case_id="case_id"></step-controller>
  </div>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';
import {handleEmpty} from "/@/utils/other";


export default defineComponent({
  name: 'preOperation',
  setup() {
    const state = reactive({
      teardown_hooks: [],
      case_id: 0,
    });

    // init suite
    const setData = (data: any, case_id: number) => {
      state.case_id = case_id
      console.log("preOperation--case_id--->", state.case_id)
      if (data) {
        state.teardown_hooks = data
      }
    }

    // 获取表单数据
    const getData = () => {
      return handleEmpty(state.teardown_hooks)
    }

    return {
      setData,
      getData,
      ...toRefs(state),
    };
  },
});
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