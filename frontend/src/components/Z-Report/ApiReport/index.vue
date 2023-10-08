<template>
  <div class="report-container">
    <el-tabs v-model="state.activeName" class="demo-tabs">
      <template v-if="state.step_type === 'api'">
        <el-tab-pane name="ResponseInfo">
          <template #label>
            <strong>响应信息</strong>
          </template>
          <ResponseInfo :data="state.responseInfo" :stat="state.stat" ref="responseInfoRef"></ResponseInfo>
        </el-tab-pane>

        <el-tab-pane name="RequestInfo">
          <template #label>
            <strong>请求信息</strong>
          </template>
          <RequestInfo :data="state.requestInfo"></RequestInfo>
        </el-tab-pane>


        <!--      <el-tab-pane label="异常信息" name="message">-->
        <!--        <request-content :data="data.req_resps[0].request"></request-content>-->
        <!--      </el-tab-pane>-->

        <el-tab-pane name="ReportVariables">
          <template #label>
            <strong>变量追踪</strong>
          </template>
          <ReportVariables :data="state.variables" ref=""></ReportVariables>
        </el-tab-pane>

         <el-tab-pane name="extracts">
          <template #label>
            <strong>参数提取
              <el-icon v-show="getExtractResultStatus !==null">
                <CircleCheck v-if="getExtractResultStatus" style="color: #0cbb52"></CircleCheck>
                <CircleClose v-else style="color: red"></CircleClose>
              </el-icon>
            </strong>
          </template>
          <ReportExtracts :data="state.extracts" :extractResults="state.extractResults"></ReportExtracts>
        </el-tab-pane>

        <el-tab-pane name="ReportValidators">
          <template #label>
            <strong>
              结果断言
              <el-icon v-show="getValidatorsResultStatus !== null">
                <CircleCheck v-if="getValidatorsResultStatus" style="color: #0cbb52"></CircleCheck>
                <CircleClose v-else style="color: red"></CircleClose>
              </el-icon>
            </strong>

          </template>
          <ReportValidators :data="state.validators" ref="validatorsRef"></ReportValidators>
        </el-tab-pane>

        <el-tab-pane name="preHookData">
          <template #label>
            <strong>Hook
              <el-icon v-show="getHookResultStatus !==null">
                <CircleCheck v-if="getHookResultStatus" style="color: #0cbb52"></CircleCheck>
                <CircleClose v-else style="color: red"></CircleClose>
              </el-icon>
            </strong>

          </template>
          <ReportHooks
              :setup-hook-results="state.setup_hook_results"
              :teardown-hook-results="state.teardown_hook_results">
          </ReportHooks>
        </el-tab-pane>
      </template>

      <el-tab-pane name="ReportLog">
        <template #label>
          <strong>运行日志</strong>
        </template>
        <ReportLog :data="state.log"></ReportLog>
      </el-tab-pane>

      <el-tab-pane label="错误信息" name="message">
        <template #label>
          <strong>错误信息</strong>
          <el-icon v-if="state.message !== ''">
            <CircleClose style="color: red"></CircleClose>
          </el-icon>
        </template>
        <ReportLog :data="state.message"></ReportLog>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script setup name="ApiReport">
import {computed, onMounted, reactive, ref, watch} from 'vue';
import {CircleCheck, CircleClose} from "@element-plus/icons";
import ResponseInfo from "./components/ResponseInfo.vue";
import RequestInfo from "./components/RequestInfo.vue";
import ReportValidators from "./components/ReportValidators.vue";
import ReportExtracts from "./components/ReportExtracts.vue";
import ReportLog from "./components/ReportLog.vue";
import ReportVariables from "./components/ReportVariables.vue";
import ReportHooks from './components/ReportHooks.vue'


const props = defineProps({
  reportData: {
    type: [Object, Array],
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
  extractResults: [],
  // 错误信息
  message: "",
  // 变量
  variables: {},
  // 日志
  log: "",
  // 错误信息
  //setup_hook
  setup_hook_results: [],
  //teardown_hook
  teardown_hook_results: [],

});

const initData = () => {
  let step_result
  if (!props.reportData.step_results) {
    step_result = props.reportData
  } else {
    let {step_results} = props.reportData
    step_result = step_results[0]
  }

  state.success = step_result.success
  state.step_type = step_result.step_type
  state.message = step_result.message
  state.log = step_result.log
  if (state.step_type === 'api') {
    state.activeName = "ResponseInfo"
    state.stat = step_result.session_data.stat
    state.responseInfo = step_result.session_data.req_resp.response
    state.requestInfo = step_result.session_data.req_resp.request
    state.validators = step_result.session_data.validators
    state.extracts = step_result.export_vars
    state.extractResults = step_result.session_data.extracts
    state.setup_hook_results = step_result.setup_hook_results
    state.teardown_hook_results = step_result.teardown_hook_results

    state.variables = {
      variables: step_result.variables,
      envVariables: step_result.env_variables,
      caseVariables: step_result.case_variables,
    }
  } else {
    state.activeName = "ReportLog"
  }

}

const getStat = () => {
  return {status_code: state.responseInfo?.status_code, ...state.stat}
}

// 获取校验结果状态
const getValidatorsResultStatus = computed(() => {
  if (!state.validators?.validate_extractor) {
    return null
  }
  if (state.validators.validate_extractor.length === 0) {
    return null
  }
  let failList = state.validators.validate_extractor.filter((e) => {
    return e.check_result !== 'pass'
  })
  return failList.length === 0
})

// 获取hook执行结果状态状态
const getHookResultStatus = computed(() => {
  if (state.setup_hook_results.length === 0 && state.teardown_hook_results.length === 0) {
    return null
  }
  let newHooks = state.setup_hook_results.concat(state.teardown_hook_results)
  let failList = newHooks.filter((e) => {
    return !e.success
  })
  return failList.length === 0
})
// 获取hook执行结果状态状态
const getExtractResultStatus = computed(() => {
  if (!state.extractResults || state.extractResults.length === 0) {
    return null
  }
  let failList = state.extractResults.filter((e) => {
    return e.extract_result !== 'pass'
  })
  return failList.length === 0
})


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