<template>
  <ExtractController :data="state.extracts"></ExtractController>
</template>

<script setup lang="ts" name="extracts">
import {defineAsyncComponent, reactive} from 'vue';
import {handleEmpty} from "/@/utils/other";

const ExtractController = defineAsyncComponent(() => import("/@/components/Z-StepController/extract/ExtractController.vue"))

const state = reactive({
  extracts: []
})

// 初始化数据
const setData = (data: any) => {
  state.extracts = data ? data : []
}

const getDataLength = () => {
  return state.extracts.length
}

// 获取表单数据
const getData = () => {
  let extractData = handleEmpty(state.extracts)
  extractData.forEach((e: any, index: number) => {
    if (e.extract_type === "") {
      throw new Error(`提取: 第${index + 1}行 提取类型不能为空~🤣`)
    }
    if (e.name === "") {
      throw new Error(`提取: 第${index + 1}行 变量名不能为空~🤣`)
    }
    if (e.path === "") {
      throw new Error(`提取: 第${index + 1}行 提取表达式不能为空~🤣`)
    }
  })
  return extractData
}

defineExpose({
  setData,
  getData,
  getDataLength,
})
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