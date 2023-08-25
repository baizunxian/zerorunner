<template>
  <HeadersController :data="state.headers"></HeadersController>
</template>

<script lang="ts" setup name="apiRequestHeaders">
import {reactive} from "vue";
import {handleEmpty} from "/@/utils/other";
import HeadersController from "/@/components/Z-StepController/headers/HeadersController.vue";


interface baseState {
  key: string,
  value: string,
  remarks: string
}

interface headersState {
  headers: Array<baseState>,
}

const state = reactive<headersState>({
  // headers
  headers: [],  // 请求头数据

});
// 初始化数据
const setData = (data: any) => {
  state.headers = data ? data : []
}

const getDataLength = () => {
  return handleEmpty(state.headers).length
}


// 获取表单数据
const getData = () => {
  return handleEmpty(state.headers)
}

// 获取是否填写状态
const getStatus = () => {
  return handleEmpty(state.headers).length > 0
}

// updateHeader {key: "Content-Type", value: "application/json"} //更新请求头
const updateHeader = (headerData: any, remove: any = false) => {
  let headerInfo = state.headers.find(e => headerData?.key && headerData.key.toLowerCase() === e.key.toLowerCase())
  if (headerInfo) {
    state.headers.forEach((e: any, index: number) => {
      if (headerData?.key && headerData.key.toLowerCase() === e.key.toLowerCase()) {
        state.headers.splice(index, 1)
        if (!remove) {
          state.headers.unshift(headerData)
        }
      }
    })
  } else {
    if (!remove) {
      state.headers.unshift(headerData)
    }
  }

}

defineExpose({
  setData,
  getData,
  updateHeader,
  getDataLength,
})


</script>

<style lang="scss" scoped>

</style>
