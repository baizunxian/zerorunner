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
                v-model:value="data.value"
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

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})


const headers = (type: string) => {
  let content = ""
  let setContent = props.data.value ? '\nzero.headers.set("key", "value")' : 'zero.headers.set("key", "value")'
  let getContent = props.data.value ? '\nzero.headers.get("key")' : 'zero.headers.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.value += content
}

// 设置环境变量
const environment = (type: string) => {
  let content = ""
  let setContent = props.data.value ? '\nzero.environment.set("key", "value")' : 'zero.environment.set("key", "value")'
  let getContent = props.data.value ? '\nzero.environment.get("key")' : 'zero.environment.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.value += content
}

const variables = (type: string) => {
  let content = ""
  let setContent = props.data.value ? '\nzero.variables.set("key", "value")' : 'zero.variables.set("key", "value")'
  let getContent = props.data.value ? '\nzero.variables.get("key")' : 'zero.variables.get("key")'
  content = type == "set" ? setContent : getContent
  props.data.value += content
}

</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}

</style>