<template>
  <variable-controller :data="variables"></variable-controller>
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

interface variablesState {
  variables: Array<baseState>,
}


export default defineComponent({
  name: 'commonConfig',
  components: {variableController},
  setup() {
    const formRef = ref()
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

    // 获取是否填写状态
    const getStatus = () => {
      return handleEmpty(state.variables).length > 0
    }

    return {
      formRef,
      setData,
      getData,
      getStatus,
      ...toRefs(state),
    };
  },
})

</script>

<style lang="scss" scoped>


</style>