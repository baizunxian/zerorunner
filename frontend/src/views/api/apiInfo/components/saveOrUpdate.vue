<template>
  <div>
    <case-info ref="caseInfoRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>

    <el-collapse-transition>
      <div v-show="showRequestBody" style="margin-bottom: 20px">
        <el-card>
          <template #header>
            <strong>Request</strong>
          </template>
          <div style="min-height: 500px">
            <el-tabs v-model="activeName" style="overflow-y: auto">
              <el-tab-pane name='requestBody'>
                <template #label>
                  <strong>请求体</strong>
                </template>
                <div class="case-tabs">
                  <request-body ref="requestBodyRef" @updateHeader="updateHeader"/>
                </div>
              </el-tab-pane>

              <el-tab-pane name='requestHeaders'>
                <template #label>
                  <el-badge :hidden="!getDataLength('header')"
                            :value="getDataLength('header')"
                            class="badge-item"
                            type="primary">
                    <strong>请求头</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <request-headers ref="headersRef"/>
                </div>
              </el-tab-pane>

              <el-tab-pane name='variablesParameters'>
                <template #label>
                  <el-badge :hidden="!getDataLength('variables')"
                            :value="getDataLength('variables')"
                            class="badge-item"
                            type="primary">
                    <strong>变量</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <variables ref="variablesRef"/>
                </div>
              </el-tab-pane>

              <el-tab-pane name='extracts' class="h100">
                <template #label>
                  <el-badge :hidden="!getDataLength('extracts')"
                            :value="getDataLength('extracts')"
                            class="badge-item" type="primary">
                    <strong>提取</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <extracts ref="extractsRef"/>
                </div>
              </el-tab-pane>

              <el-tab-pane name='preOperation' class="h100">
                <template #label>
                  <el-badge :hidden="!getDataLength('pre')"
                            :value="getDataLength('pre')"
                            class="badge-item"
                            type="primary">
                    <strong>前置操作</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <pre-steps ref="preStepsRef"/>
                </div>
              </el-tab-pane>

              <el-tab-pane name='postOperation' class="h100">
                <template #label>
                  <el-badge :hidden="!getDataLength('post')"
                            :value="getDataLength('post')"
                            class="badge-item"
                            type="primary">
                    <strong>后置操作</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <post-steps ref="postStepsRef"/>
                </div>
              </el-tab-pane>


              <el-tab-pane name='assertController' class="h100">
                <template #label>
                  <el-badge :hidden="!getDataLength('validators')"
                            :value="getDataLength('validators')"
                            class="badge-item"
                            type="primary">
                    <strong>断言规则</strong>
                  </el-badge>
                </template>
                <div class="case-tabs">
                  <validators ref="validatorsRef"/>
                </div>
              </el-tab-pane>

            </el-tabs>
          </div>
        </el-card>
      </div>
    </el-collapse-transition>


    <el-card id="Response" ref="ResponseRef" v-show="reportData">
      <template #header>
        <div style="display: flex; justify-content: space-between">
          <div>
            <strong>Response</strong>
          </div>
          <div style="font-size: 12px" v-if="apiReportStat">
            <span style="vertical-align: middle;">
              <el-icon>
                <ele-CircleCheck v-if="apiReportStat.success" style="color: #0cbb52"/>
                <ele-CircleClose v-else style="color: red"/>
              </el-icon>
              </span>
            <span style="padding-left: 10px">
              Status:
              <span :style="{color: apiReportStat.status_code === 200 ? '#67c23a': 'red'}">
                {{ apiReportStat.status_code === 200 ? '200 OK' : apiReportStat.status_code }}
                </span>
            </span>
            <span style="padding-left: 10px">Time:
            <span style="color:#67c23a;">{{ apiReportStat.response_time_ms }} ms</span>
              </span>
            <span style="padding-left: 10px">
              Size:
            <span style="color:#67c23a;">{{ formatSizeUnits(apiReportStat.content_size) }}</span>
              </span>
          </div>
        </div>
      </template>
      <div style="height: 500px; overflow-y: auto" v-show="showReport">
        <api-report v-if="showReport" :reportData="reportData" ref="apiReportRef"></api-report>
      </div>
    </el-card>

  </div>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, ref, toRefs, watch} from 'vue'
import caseInfo from '/@/views/api/apiInfo/components/apiInfo.vue'
import RequestBody from '/@/views/api/apiInfo/components/requestBody.vue'
import requestHeaders from '/@/views/api/apiInfo/components/headers.vue'
import Variables from '/@/views/api/apiInfo/components/variables.vue'
import preSteps from "/@/views/api/apiInfo/components/preSteps.vue"
import postSteps from "/@/views/api/apiInfo/components/postSteps.vue";
import validators from "/@/views/api/apiInfo/components/validators.vue";
import Extracts from "/@/views/api/apiInfo/components/extracts.vue";
import apiReport from "/@/components/Report/ApiReport/index.vue";
import {useRoute, useRouter} from "vue-router"
import {useApiInfoApi} from '/@/api/useAutoApi/apiInfo'
import {ElMessage, ElLoading} from 'element-plus'
import {formatSizeUnits} from "/@/utils/case"

export default defineComponent({
  name: 'saveOrUpdateApi',
  components: {
    Extracts,
    caseInfo,
    RequestBody,
    requestHeaders,
    Variables,
    preSteps,
    postSteps,
    validators,
    apiReport,
  },
  props: {
    case_id: Number
  },
  setup(props, {emit}) {
    const route = useRoute();
    const router = useRouter();
    const caseInfoRef = ref()
    const requestBodyRef = ref()
    const headersRef = ref()
    const preStepsRef = ref()
    const postStepsRef = ref()
    const variablesRef = ref()
    const validatorsRef = ref()
    const extractsRef = ref()
    const ResponseRef = ref()
    const apiReportRef = ref()
    const state = reactive({
      isShowDialog: false,
      activeName: 'requestBody',
      editType: '',

      // report
      showTestReportDialog: false,
      reportContent: [],

      case_id: null,

      // show
      showRequestBody: true,

      //report
      showReport: false,
      reportData: null,
      apiReportStat: null
    });


    const saveOrUpdateOrDebug = (type: string) => {
      // if (!store.state.env?.envId) {
      //   console.log("store.state.env", store.state.env)
      //   showDriver()
      //   // ElMessage.warning("请选择运行环境！")
      //   return
      // }
      try {
        let caseInfoData = caseInfoRef.value.getData()
        let bodyData = requestBodyRef.value.getData()
        let headerData = headersRef.value.getData()
        let preData = preStepsRef.value.getData()
        let postData = postStepsRef.value.getData()
        let variableData = variablesRef.value.getData()
        let validatorsData = validatorsRef.value.getData()
        let extractsData = extractsRef.value.getData()

        // 组装表单
        let apiCaseData = {
          id: state.case_id,
          name: caseInfoData.name,
          project_id: caseInfoData.project_id,
          module_id: caseInfoData.module_id,
          code_id: caseInfoData.code_id,
          code: caseInfoData.code,
          priority: caseInfoData.priority,
          method: caseInfoData.method,
          url: caseInfoData.url,
          tags: caseInfoData.tags,
          remarks: caseInfoData.remarks,
          env_id: null,
          headers: headerData,
          request_body: bodyData,
          variables: variableData,
          setup_hooks: preData,
          teardown_hooks: postData,
          validators: validatorsData,
          extracts: extractsData,
        }

        // 保存用例
        if (type === 'save') {
          useApiInfoApi().saveOrUpdate(apiCaseData)
              .then(res => {
                ElMessage.success('保存成功！')
                state.case_id = res.data
                emit("moduleChange", caseInfoData.module_id)
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
                  state.reportData = res.data
                  console.log('-----------------debug---------------')
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
      } catch (err: any) {
        console.log(err)
        ElMessage.info(err || '信息表单填写不完整')

      }
    }

    const initTestCase = () => {
      let case_id = null
      if (props.case_id) {
        case_id = props.case_id
        state.reportData = null
        state.showReport = false
      } else {
        case_id = route.query.id
      }
      console.log("case_id------>", case_id)
      if (case_id) {
        state.case_id = case_id
        useApiInfoApi().getTestCaseInfo({id: state.case_id})
            .then(res => {
              let apiCaseData = res.data
              caseInfoRef.value.setData(apiCaseData)
              requestBodyRef.value.setData(apiCaseData.request_body)
              headersRef.value.setData(apiCaseData.headers)
              variablesRef.value.setData(apiCaseData.variables)
              extractsRef.value.setData(apiCaseData.extracts)
              preStepsRef.value.setData(apiCaseData.pre_steps, state.case_id)
              postStepsRef.value.setData(apiCaseData.post_steps, state.case_id)
              validatorsRef.value.setData(apiCaseData.validators)

            })
      } else {
        state.case_id = null
        state.reportData = null
        caseInfoRef.value.setData()
        requestBodyRef.value.setData()
        headersRef.value.setData()
        variablesRef.value.setData()
        extractsRef.value.setData()
        preStepsRef.value.setData()
        postStepsRef.value.setData()
        validatorsRef.value.setData()
      }
    }

    // 返回到列表
    const goBack = () => {
      router.push({name: 'apiTestCase'})
    }

    const getDataLength = (ref: string) => {
      switch (ref) {
        case "header":
          return headersRef.value.getData().length
        case "variables":
          return variablesRef.value.getData().length
        case "pre":
          return preStepsRef.value.getData().length
        case "post":
          return postStepsRef.value.getData().length
        case "validators":
          return validatorsRef.value.getData().length
        case "extracts":
          return extractsRef.value.getData().length
      }
    }

    // updateHeader
    const updateHeader = (headerData: any, remove: any) => {
      headersRef.value.updateHeader(headerData, remove)
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
        state.apiReportStat = {...apiReportRef.value.getStat(), success: state.reportData.success}
      })
    }

    watch(
        () => props.case_id,
        () => {
          initTestCase()
        },
        {deep: true}
    )


    onMounted(() => {
      initTestCase()
    })

    return {
      caseInfoRef,
      requestBodyRef,
      headersRef,
      variablesRef,
      preStepsRef,
      postStepsRef,
      validatorsRef,
      extractsRef,
      apiReportRef,
      ResponseRef,
      route,
      router,
      goBack,
      getDataLength,
      updateHeader,
      saveOrUpdateOrDebug,
      formatSizeUnits,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-card) {
  .el-card__body {
    padding: 5px 20px;
  }
}

// el-badge
:deep(.el-badge__content) {
  border-radius: 50%;
  width: 18px;
}

:deep(.el-badge__content.is-fixed) {
  top: 8px;
  right: calc(-7px + var(--el-badge-size) / 2);
}

</style>