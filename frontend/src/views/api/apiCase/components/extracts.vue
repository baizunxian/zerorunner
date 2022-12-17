<template>
  <extract-controller :data="extracts"></extract-controller>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';
import {handleEmpty} from "/@/utils/other";
import extractController from "/@/components/StepController/extract/extractController.vue";

export default defineComponent({
  name: 'extracts',
  components: {extractController},
  setup() {
    const state = reactive({
      extracts: []
    })

    // 初始化数据
    const setData = (data: any) => {
      state.extracts = data ? data : []
      console.log("extracts----->", state.extracts)
      console.log("extracts-----data", data)
    }

    // 获取表单数据
    const getData = () => {
      return handleEmpty(state.extracts)
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

.extract-item-editing {
  padding-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  //width: 100%;

  .regex-item {
    margin-top: 10px;
  }
}

.extract-item-editing.json {
  border-left: 2px solid #44b3d2;
}

</style>