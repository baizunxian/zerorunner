<template>
  <div class="report-container">
    <el-tabs v-model="state.activeName" class="demo-tabs">
      <template v-if="state.step_type === 'api'">
        <el-tab-pane label="响应信息" name="ResponseInfo">
          <ResponseInfo :data="state.responseInfo" :stat="state.stat" ref="responseInfoRef"></ResponseInfo>
        </el-tab-pane>

        <el-tab-pane label="请求信息" name="RequestInfo">
          <RequestInfo :data="state.requestInfo"></RequestInfo>
        </el-tab-pane>

        <el-tab-pane label="结果断言" name="ReportValidators">
          <template #label>
            <span>结果断言</span>
            <el-icon v-show="getValidatorsResult() !== ''">
              <ele-CircleCheck v-if="getValidatorsResult() === 'pass'" style="color: #0cbb52"/>
              <ele-CircleClose v-else style="color: red"/>
            </el-icon>
          </template>
          <ReportValidators :data="state.validators" ref="validatorsRef"></ReportValidators>
        </el-tab-pane>

        <el-tab-pane label="参数提取" name="extracts">
          <ReportExtracts :data="state.extracts"></ReportExtracts>
        </el-tab-pane>

        <!--      <el-tab-pane label="异常信息" name="message">-->
        <!--        <request-content :data="data.req_resps[0].request"></request-content>-->
        <!--      </el-tab-pane>-->

        <el-tab-pane label="变量追踪" name="ReportVariables">
          <ReportVariables :data="state.variables" ref=""></ReportVariables>
        </el-tab-pane>


<!--        <el-tab-pane name="preHookData">-->
<!--          <template #label>-->
<!--            <span>前置步骤</span>-->
<!--            <el-icon v-show="state.pre_hook_status !== ''">-->
<!--              <ele-CircleCheck v-if="state.pre_hook_status === 'success'" style="color: #0cbb52"/>-->
<!--              <ele-CircleClose v-else style="color: red"/>-->
<!--            </el-icon>-->
<!--          </template>-->
<!--          <ReportStepInfo :data="state.pre_hook_data"></ReportStepInfo>-->
<!--        </el-tab-pane>-->

<!--        <el-tab-pane name="postHookData">-->
<!--          <template #label>-->
<!--            <span>后置步骤</span>-->
<!--            <el-icon v-show="state.post_hook_status !== ''">-->
<!--              <ele-CircleCheck v-if="state.post_hook_status ==='success'" style="color: #0cbb52"/>-->
<!--              <ele-CircleClose v-else style="color: red"/>-->
<!--            </el-icon>-->
<!--          </template>-->
<!--          <ReportStepInfo :data="state.post_hook_data"></ReportStepInfo>-->
<!--        </el-tab-pane>-->

      </template>

      <el-tab-pane label="运行日志" name="ReportLog">
        <ReportLog :data="state.log"></ReportLog>
      </el-tab-pane>

      <el-tab-pane label="错误信息" name="message">
        <template #label>
          <span>错误信息</span>
          <el-icon v-if="state.message !== ''">
            <ele-CircleClose style="color: red"/>
          </el-icon>
        </template>
        <ReportLog :data="state.message"></ReportLog>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script lang="ts" setup name="ApiReport">
import {onMounted, PropType, reactive, ref, watch} from 'vue';
import ResponseInfo from "./ResponseInfo.vue";
import RequestInfo from "./RequestInfo.vue";
import ReportValidators from "./ReportValidators.vue";
import ReportExtracts from "./ReportExtracts.vue";
import ReportLog from "./ReportLog.vue";
import ReportVariables from "./ReportVariables.vue";
import ReportStepInfo from "./ReportStepInfo.vue";


const props = defineProps({
  reportData: {
    type: [Object, Array] as PropType<ReportData>,
    required: true
  }
},)


const responseInfoRef = ref()
const validatorsRef = ref()
const state = reactive({
  // data
  activeName: "ResponseInfo",
  // 是否成功
  success: false,
  stat: {},
  // 步骤类型
  step_type: "",
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
  let step_data: StepData
  if (!props.reportData.step_datas) {
    step_data = props.reportData
  } else {
    let {step_datas} = props.reportData
    step_data = step_datas[0]
  }

  state.success = step_data.success
  state.step_type = step_data.step_type
  state.message = step_data.message
  state.log = props.reportData.log
  if (state.step_type == 'api') {
    state.activeName = "ResponseInfo"
    state.stat = step_data.session_data.stat
    state.responseInfo = step_data.session_data.req_resp.response
    state.requestInfo = step_data.session_data.req_resp.request
    state.validators = step_data.session_data.validators
    state.extracts = step_data.export_vars
    state.post_hook_data = step_data.post_hook_data
    state.pre_hook_data = step_data.pre_hook_data
    state.pre_hook_status = getHookStatus(state.pre_hook_data)
    state.post_hook_status = getHookStatus(state.post_hook_data)
    state.variables = {
      variables: step_data.variables,
      envVariables: step_data.env_variables,
      caseVariables: step_data.case_variables,
    }
  } else {
    state.activeName = "ReportLog"
  }

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


defineExpose({
  getStat,
})

</script>

<style lang="scss" scoped>
.report-container {
  padding: 10px;
}
</style>