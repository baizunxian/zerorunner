<template>
  <variable-controller :data="variables"></variable-controller>
</template>

<script lang="ts">

import {handleEmpty} from "/@/utils/other";
import {defineComponent, reactive, toRefs} from "vue";
import variableController from "/@/components/StepController/variable/variableController.vue";

interface baseState {
  key: string,
  value: string,
  remarks: string
}

interface variablesState {
  variables: Array<baseState>,
}


export default defineComponent({
  name: 'commonConfig',
  components: {variableController},
  setup() {
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

    return {
      setData,
      getData,
      ...toRefs(state),
    };
  },
})

</script>

<style lang="scss" scoped>


</style>