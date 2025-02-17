<template>
  <div>
    <el-row>
      <el-col :span="18">
        <div style="border: 1px solid #E6E6E6">
          <z-monaco-editor
              style="height: 500px"
              ref="monacoEditRef"
              v-model:value="o_content"
              :options="{minimap: {enabled: false}}"
          />
        </div>
      </el-col>

      <el-col :span="6">
        <div style="padding: 8px;">
          <div>代码片段</div>
          <div>
            <el-button type="primary" link @click="headers('get')">获取请求头</el-button>
          </div>
          <div>
            <el-button type="primary" link @click="environment('get')">获取环境变量</el-button>
          </div>
          <div>
            <el-button type="primary" link @click="variables('get')">获取变量</el-button>
          </div>
          <div>
            <el-button type="primary" link @click="headers('set')">设置请求头</el-button>
          </div>
          <div>
            <el-button type="primary" link @click="environment('set')">设置环境变量</el-button>
          </div>
          <div>
            <el-button type="primary" link @click="variables('set')">设置变量</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="ScriptController">

import {computed, reactive} from "vue";

const emit = defineEmits(['update:codeContent'])

const props = defineProps({
  codeContent: {
    type: String,
    default: () => {
      return ""
    }
  }
})

const o_content = computed({
      get() {
        return props.codeContent
      },
      set(val) {
        emit("update:codeContent", val)
      }
    }
)

const state = reactive({
  content: o_content.value
})


const headers = (type) => {
  let content
  let setContent = o_content.value ? '\nzero.headers.set("key", "value")' : 'zero.headers.set("key", "value")'
  let getContent = o_content.value ? '\nzero.headers.get("key")' : 'zero.headers.get("key")'
  content = type === "set" ? setContent : getContent
  o_content.value = o_content.value + content
  console.log(props.codeContent, "codeContent")
  console.log(o_content.value, "o_content")
}

// 设置环境变量
const environment = (type) => {
  let content
  let setContent = o_content.value ? '\nzero.environment.set("key", "value")' : 'zero.environment.set("key", "value")'
  let getContent = o_content.value ? '\nzero.environment.get("key")' : 'zero.environment.get("key")'
  content = type === "set" ? setContent : getContent
  o_content.value += content
}

const variables = (type) => {
  let content
  let setContent = o_content.value ? '\nzero.variables.set("key", "value")' : 'zero.variables.set("key", "value")'
  let getContent = o_content.value ? '\nzero.variables.get("key")' : 'zero.variables.get("key")'
  content = type === "set" ? setContent : getContent
  o_content.value += content
}


// onMounted(() => {
//   if (!props.data.script_request) {
//     props.data.script_request = {
//       script_content: ""
//     }
//   }
// })
</script>

<style lang="scss" scoped>


</style>