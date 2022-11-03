<template>
<!--  <el-collapse-transition>-->
    <div v-if="data.req_resps.length === 1" style="height: 300px">
      <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="响应体" name="responseBody">
          <response-body :data="data.req_resps[0].response"></response-body>
        </el-tab-pane>

        <el-tab-pane label="响应头" name="responseHeader">
          <response-header :data="data.req_resps[0].response"></response-header>
        </el-tab-pane>

        <el-tab-pane label="断言" name="validators">
          <validators :data="data.validators"></validators>
        </el-tab-pane>

        <el-tab-pane label="提取" name="extracts">
          <extracts :data="data.export_vars"></extracts>
        </el-tab-pane>

        <el-tab-pane label="请求内容" name="requestContent">
          <request-content :data="data.req_resps[0].request"></request-content>
        </el-tab-pane>
      </el-tabs>
    </div>

<!--  </el-collapse-transition>-->
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';
import responseBody from "/@/components/Report/ApiReport/responseBody.vue";
import responseHeader from "/@/components/Report/ApiReport/responseHeader.vue";
import validators from "/@/components/Report/ApiReport/validators.vue";
import extracts from "/@/components/Report/ApiReport/extracts.vue";
import requestContent from "/@/components/Report/ApiReport/requestContent.vue";


export default defineComponent({
  name: 'reportDetail',
  components: {
    responseBody,
    responseHeader,
    validators,
    extracts,
    requestContent,
  },
  props: {
    data: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  setup(props: any) {
    const state = reactive({
      // data
      activeName: "responseBody"

    });


    return {
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>

</style>