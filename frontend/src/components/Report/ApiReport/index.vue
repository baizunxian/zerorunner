<template>
  <div class="report-container">
    <el-tabs v-model="activeName" class="demo-tabs">
      <el-tab-pane label="响应信息" name="responseInfo">
        <response-info :data="responseInfo" :stat="stat" ref="responseInfoRef"></response-info>
      </el-tab-pane>

      <el-tab-pane label="请求信息" name="requestInfo">
        <request-info :data="requestInfo"></request-info>
      </el-tab-pane>

      <el-tab-pane label="结果验证" name="validators">
        <template #label>
          <span>结果验证</span>
          <el-icon v-show="getValidatorsResult() !== ''">
            <ele-CircleCheck v-if="getValidatorsResult() === 'pass'" style="color: #0cbb52"/>
            <ele-CircleClose v-else style="color: red"/>
          </el-icon>
        </template>
        <validators :data="validators" ref="validatorsRef"></validators>
      </el-tab-pane>

      <el-tab-pane label="参数提取" name="extracts">
        <extracts :data="extracts"></extracts>
      </el-tab-pane>

      <!--      <el-tab-pane label="异常信息" name="message">-->
      <!--        <request-content :data="data.req_resps[0].request"></request-content>-->
      <!--      </el-tab-pane>-->

      <el-tab-pane label="变量追踪" name="variables">
        <variables :data="variables" ref=""></variables>
      </el-tab-pane>


      <el-tab-pane name="preHookData">
        <template #label>
          <span>前置步骤</span>
          <el-icon v-show="pre_hook_status !== ''">
            <ele-CircleCheck v-if="pre_hook_status === 'success'" style="color: #0cbb52"/>
            <ele-CircleClose v-else style="color: red"/>
          </el-icon>
        </template>
        <step-info :data="pre_hook_data"></step-info>
      </el-tab-pane>

      <el-tab-pane name="postHookData">
        <template #label>
          <span>后置步骤</span>
          <el-icon v-show="post_hook_status !== ''">
            <ele-CircleCheck v-if="post_hook_status ==='success'" style="color: #0cbb52"/>
            <ele-CircleClose v-else style="color: red"/>
          </el-icon>
        </template>
        <step-info :data="post_hook_data"></step-info>
      </el-tab-pane>

      <el-tab-pane label="运行日志" name="log">
        <log :data="log"></log>
      </el-tab-pane>

      <el-tab-pane label="错误信息" name="message">
        <template #label>
          <span>错误信息</span>
          <el-icon v-if="message !== ''">
            <ele-CircleClose style="color: red"/>
          </el-icon>
        </template>
        <log :data="message"></log>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs, ref, watch, nextTick} from 'vue';
import responseInfo from "/@/components/Report/ApiReport/responseInfo.vue";
import requestInfo from "/@/components/Report/ApiReport/requestInfo.vue";
import validators from "/@/components/Report/ApiReport/validators.vue";
import extracts from "/@/components/Report/ApiReport/extracts.vue";
import log from "/@/components/Report/ApiReport/log.vue";
import variables from "/@/components/Report/ApiReport/variables.vue";
import stepInfo from "/@/components/Report/ApiReport/stepInfo.vue";
import type {StepDatas} from "/@/components/Report/ApiReport/apiReport";

export default defineComponent({
  name: 'apiReport',
  components: {
    responseInfo,
    requestInfo,
    validators,
    extracts,
    variables,
    log,
    stepInfo,
  },
  props: {
    reportData: {
      type: [Object, Array],
      required: true
      // default: () => {
      //   return {}
      // }
    }
  },
  setup(props: any) {
    const responseInfoRef = ref()
    const validatorsRef = ref()
    const state = reactive({
      // data
      activeName: "responseInfo",
      // 是否成功
      success: false,
      stat: {},
      // 响应信息
      responseInfo: {},
      // 请求信息
      requestInfo: {},
      // 结果校验
      validators: {},
      validatorsResult: "",
      // 参数提取
      extracts: {},
      // 错误信息
      message: "",
      // 变量
      variables: {},
      // 日志
      log: "",
      // 错误信息
      //前置步骤
      post_hook_data: [],
      post_hook_status: "",
      //后置步骤
      pre_hook_data: [],
      pre_hook_status: "",

    });

    const initData = () => {
      let step_data: StepDatas
      if (!props.reportData.step_datas) {
        step_data = props.reportData
      } else {
        let {step_datas} = props.reportData
        step_data = step_datas[0]
      }

      state.success = step_data.success
      state.stat = step_data.session_data.stat
      state.responseInfo = step_data.session_data.req_resp.response
      state.requestInfo = step_data.session_data.req_resp.request
      state.validators = step_data.session_data.validators
      state.extracts = step_data.export_vars
      state.message = step_data.message
      state.variables = {
        variables: step_data.variables,
        envVariables: step_data.env_variables,
      }
      state.log = props.reportData.log
      state.post_hook_data = step_data.post_hook_data
      state.pre_hook_data = step_data.pre_hook_data
      state.pre_hook_status = getHookStatus(state.pre_hook_data)
      state.post_hook_status = getHookStatus(state.post_hook_data)

    }

    const getStat = () => {
      return {status_code: state.responseInfo.status_code, ...state.stat}
    }
    const getValidatorsResult = () => {
      return validatorsRef.value.validatorsResult()
    }

    const getHookStatus = (hook: Array<any>) => {
      if (hook.length === 0) return ""
      let success_count = 0
      hook.forEach((h) => {
        if (h.success) success_count++
      })
      if (success_count == hook.length) return "success"
      return "fail"
    }


    watch(
        () => props.reportData,
        () => {
          initData()
        },
        {deep: true}
    );

    onMounted(() => {
      initData()
    })

    return {
      getStat,
      validatorsRef,
      responseInfoRef,
      getHookStatus,
      initData,
      getValidatorsResult,
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>
.report-container {
  padding: 10px;
}
</style>