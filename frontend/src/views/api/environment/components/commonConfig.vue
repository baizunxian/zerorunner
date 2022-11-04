<template>
  <variable-controller :data="data.variables"></variable-controller>
</template>

<script lang="ts">

import {handleEmpty} from "/@/utils/other";
import {defineComponent, reactive, ref, toRefs} from "vue";
import variableController from "/@/components/StepController/variableController.vue";

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


</style>