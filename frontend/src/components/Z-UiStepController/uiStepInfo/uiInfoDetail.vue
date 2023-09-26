<template>
  <div class="app-container">
    <el-card>
      <UiInfo ref="UiInfoRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>
      <el-card>
        <template #header>
          <strong>操作</strong>
        </template>
        <div style="min-height: 500px">
          <el-tabs>
<!--            <el-tab-pane name='ApiVariables'>-->
<!--              <template #label>-->
<!--                <strong>变量</strong>-->
<!--                <span class="ui-badge-circle" v-show="getDataLength('variables')">{{-->
<!--                    getDataLength('variables')-->
<!--                  }}</span>-->
<!--              </template>-->
<!--              <div class="case-tabs">-->
<!--                <ApiVariables ref="ApiVariablesRef"/>-->
<!--              </div>-->
<!--            </el-tab-pane>-->

<!--            <el-tab-pane name='extracts' class="h100">-->
<!--              <template #label>-->
<!--                <strong>提取</strong>-->
<!--                <span class="ui-badge-circle" v-show="getDataLength('extracts')">{{-->
<!--                    getDataLength('extracts')-->
<!--                  }}</span>-->
<!--              </template>-->
<!--              <div class="case-tabs">-->
<!--                <ApiExtracts ref="ApiExtractsRef"/>-->
<!--              </div>-->
<!--            </el-tab-pane>-->

<!--            <el-tab-pane name='Code' class="h100">-->
<!--              <template #label>-->
<!--                <strong>Code</strong>-->
<!--                <span class="ui-badge-status-dot" v-show="getDataLength('code')"></span>-->
<!--              </template>-->
<!--              <ApiCode ref="ApiCodeRef"/>-->
<!--            </el-tab-pane>-->

<!--            <el-tab-pane name='Hook' class="h100">-->
<!--              <template #label>-->
<!--                <strong>Hook</strong>-->
<!--                <span class="ui-badge-circle" v-show="getDataLength('hook')">{{ getDataLength('hook') }}</span>-->
<!--              </template>-->
<!--              <ApiHooks ref="ApiHookRef"/>-->
<!--            </el-tab-pane>-->

<!--            <el-tab-pane name='assertController' class="h100">-->
<!--              <template #label>-->
<!--                <strong>断言规则</strong>-->
<!--                <span class="ui-badge-circle" v-show="getDataLength('validators')">{{-->
<!--                    getDataLength('validators')-->
<!--                  }}</span>-->
<!--              </template>-->
<!--              <div class="case-tabs">-->
<!--                <ApiValidators ref="ApiValidatorsRef"/>-->
<!--              </div>-->
<!--            </el-tab-pane>-->
          </el-tabs>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup name="ApiSaveOrUpdate">
import {defineProps, nextTick, onMounted, reactive, ref, watch} from 'vue'
import {useRoute, useRouter} from "vue-router"
import {useApiInfoApi} from '/@/api/useAutoApi/apiInfo'
import {ElLoading, ElMessage} from 'element-plus'

import UiInfo from './uiInfo.vue'

// 定义父组件传过来的值
const props = defineProps({
  api_id: {
    type: [String, Number],
    default: () => {
      return null;
    },
  },
  isView: {
    type: Boolean,
    default: () => {
      return false;
    },
  },
});

const route = useRoute();
const router = useRouter();

const ApiInfoRef = ref()
const ApiRequestBodyRef = ref()
const ApiRequestHeadersRef = ref()
const ApiVariablesRef = ref()
const ApiValidatorsRef = ref()
const ApiExtractsRef = ref()
const ResponseRef = ref()
const ApiReportRef = ref()
// const APiSetupHooksRef = ref()
// const APiTeardownHooksRef = ref()
const ApiCodeRef = ref()
const ApiHookRef = ref()

const state = reactive({
  isShowDialog: false,
  activeName: 'ApiRequestBody',
  editType: '',

  // report
  showTestReportDialog: false,
  reportContent: [],

  api_id: null,

  // show
  showRequestBody: true,

  //report
  showReport: false,
  reportData: null,
  apiReportStat: null,
});


const saveOrUpdateOrDebug = (type) => {
  // if (!store.state.env?.envId) {
  //   console.log("store.state.env", store.state.env)
  //   showDriver()
  //   // ElMessage.warning("请选择运行环境！")
  //   return
  // }
  try {

    let caseInfoData = ApiInfoRef.value.getData()
    let bodyData = ApiRequestBodyRef.value.getData()
    let headerData = ApiRequestHeadersRef.value.getData()
    let variableData = ApiVariablesRef.value.getData()
    let validatorsData = ApiValidatorsRef.value.getData()
    let extractsData = ApiExtractsRef.value.getData()
    let hookData = ApiHookRef.value.getData()
    let codeData = ApiCodeRef.value.getData()

    // 组装表单
    let apiCaseData = {
      id: state.api_id,
      name: caseInfoData.name,
      project_id: caseInfoData.project_id,
      module_id: caseInfoData.module_id,
      code_id: caseInfoData.code_id,
      code: caseInfoData.code,
      priority: caseInfoData.priority,
      method: caseInfoData.method,
      url: caseInfoData.url,
      tags: caseInfoData.tags,
      step_type: "api",
      remarks: caseInfoData.remarks,
      env_id: caseInfoData.env_id,
      request: {
        ...bodyData,
        headers: headerData,
        method: caseInfoData.method,
        url: caseInfoData.url,
      },
      variables: variableData,
      setup_code: codeData.setup_code,
      teardown_code: codeData.teardown_code,
      validators: validatorsData,
      extracts: extractsData,
      setup_hooks: hookData.setup_hooks,
      teardown_hooks: hookData.teardown_hooks,
    }

    // 保存用例
    if (type === 'save') {
      useApiInfoApi().saveOrUpdate(apiCaseData)
        .then(res => {
          ElMessage.success('保存成功！')
          state.api_id = res.data.id
        })
    } else {
      // testCaseData.type = type
      // testCaseData.base_url = urlForm.base_url
      const loading = ElLoading.service({
        lock: true,
        text: '用例执行中,请稍候。。。',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.8)',
        customClass: 'loading-class'
      })
      useApiInfoApi().debugApi(apiCaseData)
        .then(res => {
          state.reportData = null

          if (type === 'debug') {
            console.log('-----------------debug---------------')
            state.reportData = res.data
            state.showReport = true
            toResponse()
            loading.close()
          } else {
            // this.drawer = true
            loading.close()
          }
        })
        .catch(() => {
          loading.close()
        })
    }
  } catch (err) {
    console.log(err)
    ElMessage.warning(err.message || '信息表单填写不完整')

  }
}

const initApi = () => {
  let api_id
  if (props.api_id) {
    api_id = props.api_id
    state.reportData = null
    state.showReport = false
  } else {
    api_id = route.query.id
  }
  console.log("api_id------>", api_id)
  if (api_id) {
    state.api_id = api_id
    useApiInfoApi().getApiInfo({id: state.api_id})
      .then(res => {
        let apiCaseData = res.data
        ApiInfoRef.value.setData(apiCaseData)
        ApiRequestBodyRef.value.setData(apiCaseData.request)
        ApiRequestHeadersRef.value.setData(apiCaseData.headers)
        ApiVariablesRef.value.setData(apiCaseData.variables)
        ApiExtractsRef.value.setData(apiCaseData.extracts)
        ApiValidatorsRef.value.setData(apiCaseData.validators)
        ApiCodeRef.value.setData(apiCaseData.setup_code, apiCaseData.teardown_code)
        // APiSetupHooksRef.value.setData(apiCaseData.setup_hooks, state.api_id)
        // APiTeardownHooksRef.value.setData(apiCaseData.teardown_hooks, state.api_id)
        ApiHookRef.value.setData(apiCaseData.setup_hooks, apiCaseData.teardown_hooks, state.api_id)

      })
  } else {
    state.api_id = null
    state.reportData = null
    ApiInfoRef.value.setData()
    ApiRequestBodyRef.value.setData()
    ApiRequestHeadersRef.value.setData()
    ApiVariablesRef.value.setData()
    ApiExtractsRef.value.setData()
    ApiValidatorsRef.value.setData()
    ApiCodeRef.value.setData()
    ApiHookRef.value.setData()
    // APiSetupHooksRef.value.setData()
    // APiTeardownHooksRef.value.setData()
  }
}

// 返回到列表
const goBack = () => {
  router.push({name: 'apiInfo'})
}

const getDataLength = (ref) => {
  switch (ref) {
    case "body":
      return ApiRequestBodyRef?.value.getDataLength()
    case "header":
      return ApiRequestHeadersRef?.value.getDataLength()
    case "variables":
      return ApiVariablesRef.value.getDataLength()
    case "validators":
      return ApiValidatorsRef.value.getDataLength()
    case "extracts":
      return ApiExtractsRef.value.getDataLength()
    case "hook":
      return ApiHookRef.value.getDataLength()
    case "code":
      return ApiCodeRef.value.getDataLength()
    default:
      return 0
  }
}

// updateHeader
const updateHeader = (headerData, remove) => {
  ApiRequestHeadersRef.value.updateHeader(headerData, remove)
}

const toResponse = () => {
  nextTick(() => {
    ResponseRef.value.$el.scrollIntoView({
      behavior: "smooth",
      // 定义动画过渡效果， "auto"或 "smooth" 之一。默认为 "auto"
      block: "center",
      // 定义垂直方向的对齐， "start", "center", "end", 或 "nearest"之一。默认为 "start"
      inline: "nearest"
    })
    state.apiReportStat = {...ApiReportRef.value.getStat(), success: state.reportData.success}
  })
}

watch(
  () => props.api_id,
  () => {
    initApi()
  },
)

onMounted(() => {
  initApi()
})

</script>

<style lang="scss" scoped>

// el-badge
:deep(.el-badge__content) {
  border-radius: 50%;
  width: 18px;
}

:deep(.el-badge__content.is-fixed) {
  top: 10px;
  right: calc(-7px + var(--el-badge-size) / 2);
}

</style>