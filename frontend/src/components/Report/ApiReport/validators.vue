<template>
  <el-table :data="data.validate_extractor">
    <el-table-column prop="check" label="断言名称"></el-table-column>
    <el-table-column prop="check_value" label="断言值"></el-table-column>
    <el-table-column prop="expect" label="期望"></el-table-column>
    <el-table-column prop="expect_value" label="期望值"></el-table-column>
    <el-table-column prop="check_result" label="断言结果"></el-table-column>
    <el-table-column prop="message" label="错误信息"></el-table-column>
  </el-table>
</template>

<script lang="ts">
import {defineComponent} from 'vue';


export default defineComponent({
  name: 'scriptController',
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup(props: any) {
    // 设置请求头
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

    // 删除节点
    return {
      headers,
      environment,
      variables,
    };
  },
});
</script>

<style lang="scss" scoped>

</style>