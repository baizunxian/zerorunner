<template>
  <pre>
    {{ getContent() }}
  </pre>
</template>

<script lang="ts">
import {defineComponent} from 'vue';


export default defineComponent({
  name: 'scriptController',
  props: {
    data: Object
  },
  setup(props: any) {

    const getContent = () => {
      let url = props.data.url
      let method = props.data.method
      let headersStr = getStr(props.data.headers)
      let cookiesStr = getStr(props.data.cookies)
      let bodyStr = getBody(props.data.body)
      let content = `请求头地址:\n${url}\n\n` +
          `请求头：\n ${headersStr} \n\n` +
          `Cookies:\n${cookiesStr}\n\n` +
          `Body:\n${method}:${url}\n\n` +
          `${method} data:\n${bodyStr}\n`

      return content
    }

    const getStr = (dataContent: Object) => {
      console.log("datadatadatadatadatadatadata", dataContent)
      let Str = ""
      if (typeof dataContent === "Object") {
        dataContent.forEach((key: any, value: any) => {
          Str += `${key}:${value}\n`
        })
      }

      return Str
    }

    const getBody = (body: any) => {
      try {
        return JSON.stringify(body)
      } catch (e) {
        return body
      }
    }
    // 删除节点
    return {
      getContent
    };
  },
});
</script>

<style lang="scss" scoped>

</style>