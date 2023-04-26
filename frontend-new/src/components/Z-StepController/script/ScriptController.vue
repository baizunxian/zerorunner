<template>
  <el-collapse-transition>
    <div v-show="data.showDetail" @click.stop="">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <el-row class="controller-content">
        <el-col :span="18">
          <div style="border: 1px solid #E6E6E6">
            <z-monaco-editor
                style="height: 500px"
                ref="monacoEditRef"
                v-model:value="data.script_request.script_content"
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
  </el-collapse-transition>
</template>

<script lang="ts" setup name="ScriptController">

import {onMounted, PropType} from "vue";

const props = defineProps({
  data: {
    type: Object as PropType<TStepDataStat>,
    required: true,
  }
})


const headers = (type: string) => {
   let content: string
  let setContent = props.data.script_request?.script_content ? '\nzero.headers.set("key", "value")' : 'zero.headers.set("key", "value")'
  let getContent = props.data.script_request?.script_content ? '\nzero.headers.get("key")' : 'zero.headers.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.script_request.script_content += content
}

// 设置环境变量
const environment = (type: string) => {
   let content: string
  let setContent = props.data.script_request?.script_content ? '\nzero.environment.set("key", "value")' : 'zero.environment.set("key", "value")'
  let getContent = props.data.script_request?.script_content ? '\nzero.environment.get("key")' : 'zero.environment.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.script_request.script_content += content
}

const variables = (type: string) => {
  let content: string
  let setContent = props.data.script_request?.script_content ? '\nzero.variables.set("key", "value")' : 'zero.variables.set("key", "value")'
  let getContent = props.data.script_request?.script_content ? '\nzero.variables.get("key")' : 'zero.variables.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.script_request.script_content += content
}


onMounted(() => {
  if (!props.data.script_request) {
    props.data.script_request = {
      script_content: ""
    }
  }
})
</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}

</style>