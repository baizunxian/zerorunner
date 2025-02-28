<template>
  <HeadersController v-model:data="state.headers"></HeadersController>
</template>

<script setup name="apiRequestHeaders">
import {reactive} from "vue";
import {handleEmpty} from "/@/utils/other";
import HeadersController from "/@/components/Z-StepController/headers/HeadersController.vue";

const state = reactive({
  // headers
  headers: [],  // 请求头数据

});
// 初始化数据
const setData = (data) => {
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
const updateContentType = (mode, language, remove) => {
  let headerValue = ""
  switch (mode) {
    case "form_data":
      headerValue = ""
      break
    case "x_www_form_urlencoded":
      headerValue = "application/x-www-form-urlencoded"
      break
    case "raw":
      language = language.toLowerCase()
      if (language === "json") {
        headerValue = "application/json"
      } else if (language === "xml") {
        headerValue = "application/xml"
      } else if (language === "html") {
        headerValue = "text/html"
      } else if (language === "text") {
        headerValue = "text/plain"
      }
      break
  }
  let contentType = state.headers.find(e => e.key.toLowerCase() === "content-type")
  if (contentType) {
    if (contentType.value.toLowerCase() !== headerValue.toLowerCase()) {
      contentType.value = headerValue
    }
  } else {
    if (headerValue) {
      state.headers.unshift({key: "Content-Type", value: headerValue, remarks: ""})
    }
  }
  if (remove) {
    state.headers = state.headers.filter(e => e.key.toLowerCase() !== "content-type")
  }
}

defineExpose({
  setData,
  getData,
  updateContentType,
  getDataLength,
})


</script>

<style lang="scss" scoped>

</style>
