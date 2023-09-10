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
          <div v-for="menu in sideMenu" :key="menu.label">
            <el-button type="primary" link @click="handlerCode(menu)">{{ menu.label }}</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup name="ScriptController">

import {computed, reactive} from "vue";

const emit = defineEmits(['update:codeContent'])

const props = defineProps({
  useType: {
    type: String,
    default: () => {
      return "setup"
    }
  },
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
      set(val: any) {
        emit("update:codeContent", val)
      }
    }
)

const state = reactive({
  content: o_content.value,
  setupMenu: [
    {label: "获取请求头", content: "zero.request.headers.get('key')"},
    {label: "获取环境变量", content: "zero.environment.get('key')"},
    {label: "获取变量", content: "zero.variables.get('key')"},
    {label: "设置请求头", content: "zero.request.headers.set('key', 'value')"},
    {label: "设置环境变量", content: "zero.environment.set('key', 'value')"},
    {label: "设置变量", content: "zero.variables.set('key', 'value')"},
    {label: "打印日志", content: "logger.info('logger')"},
  ],
  teardownMenu: [
    // {label: "获取请求头", content: "zero.headers.get('key')"},
    // {label: "获取环境变量", content: "zero.environment.get('key')"},
    {label: "获取变量", content: "zero.variables.get('key')"},
    // {label: "设置请求头", content: "zero.request.headers.set('key', 'value')"},
    // {label: "设置环境变量", content: "zero.environment.set('key', 'value')"},
    {label: "设置变量", content: "zero.variables.set('key', 'value')"},
    {label: "打印日志", content: "logger.info('logger')"},
  ],

})

const sideMenu = computed(() => {
  return props.useType === "setup" ? state.setupMenu : state.teardownMenu
})

// 处理code
const handlerCode = (row: any) => {
  o_content.value = o_content.value ? o_content.value + `\n${row.content}` : row.content
}

</script>

<style lang="scss" scoped>


</style>