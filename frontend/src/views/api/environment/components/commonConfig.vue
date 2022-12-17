<template>
  <div class="content">
    <div class="block-title">环境变量</div>
    <variable-controller :data="data.variables"></variable-controller>
  </div>
</template>

<script lang="ts">

import {handleEmpty} from "/@/utils/other";
import {defineComponent, reactive, ref, toRefs} from "vue";
import variableController from "/@/components/StepController/variable/variableController.vue";

interface baseState {
  key: string,
  value: string,
  remarks: string
}

interface dataState {
  variables: Array<baseState>,
}

interface state {
  data: dataState
}

export default defineComponent({
  name: 'commonConfig',
  components: {variableController},
  setup() {
    const formRef = ref()
    const state = reactive<state>({
      data: {
        variables: [],   // 变量列表
      },
    });
    // 初始化数据
    const setData = (data: any) => {
      if (data?.variables) {
        state.data.variables = data.variables
      }
    }

    // 获取表单数据
    const getData = () => {
      state.data.variables = handleEmpty(state.data.variables)
      return state.data
    }

    return {
      formRef,
      setData,
      getData,

      ...toRefs(state),
    };
  },
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