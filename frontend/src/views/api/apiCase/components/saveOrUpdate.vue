<template>
  <div class="save-update-card">
    <div>
      <el-page-header
          class="page-header"
          style="padding-bottom: 10px"
          @back="goBack"
      >
        <template #content>
          <span>{{editType === 'create'? '新增用例':'更新用例'}}</span>
        </template>
        <template #extra>
          <el-button type="success" @click="saveOrUpdateOrDebug('debug')">调试</el-button>
          <el-button type="primary" @click="saveOrUpdateOrDebug('save')" class="title-button">保存</el-button>
        </template>
      </el-page-header>

      <h3 class="block-title">请求信息</h3>

      <url ref="urlRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>

      <h3 class="block-title">基本信息</h3>

      <messages ref="messagesRef"/>

      <h3 class="block-title">请求参数</h3>
      <div style="min-height: 500px">
        <el-tabs v-model="activeName">
          <el-tab-pane name='requestBody'>
            <template #label>
              <div style="align-items: center; display: flex; justify-content: center">
                <strong>请求体</strong>
                <div v-show="getStatus('body')" class="request-editor-tabs-badge"></div>
              </div>
            </template>
            <div class="case-tabs">
              <request-body ref="requestBodyRef" @updateHeader="updateHeader"/>
            </div>
          </el-tab-pane>

          <el-tab-pane name='requestHeaders'>
            <template #label><strong>请求头

              <div class="el-step__icon is-text zh-header" v-show="getDataLength('header')">
                <div class="el-step__icon-inner">{{ getDataLength('header') }}</div>
              </div>

            </strong></template>
            <div class="case-tabs">
              <request-headers ref="headersRef"/>
            </div>
          </el-tab-pane>

          <el-tab-pane name='variablesParameters'>
            <template #label>
              <div style="align-items: center; display: flex; justify-content: center">
                <strong>变量</strong>
                <div class="el-step__icon is-text zh-header" v-show="getDataLength('variables')">
                  <div class="el-step__icon-inner">{{ getDataLength('variables') }}</div>
                </div>
              </div>
            </template>
            <div class="case-tabs">
              <variables ref="variablesRef"/>
            </div>
          </el-tab-pane>

          <el-tab-pane name='preOperation' class="h100">
            <template #label>
              <div style="align-items: center; display: flex; justify-content: center">
                <strong>前置操作</strong>
                <div class="el-step__icon is-text zh-header" v-show="getDataLength('pre')">
                  <div class="el-step__icon-inner">{{ getDataLength('pre') }}</div>
                </div>
              </div>
            </template>
            <div class="case-tabs">
              <pre-operation ref="preOperationRef"/>
            </div>
          </el-tab-pane>

          <el-tab-pane name='postOperation' class="h100">
            <template #label>
              <div style="align-items: center; display: flex; justify-content: center">
                <strong>后置操作</strong>
                <div class="el-step__icon is-text zh-header" v-show="getDataLength('post')">
                  <div class="el-step__icon-inner">{{ getDataLength('post') }}</div>
                </div>
              </div>
            </template>
            <div class="case-tabs">
              <post-operation ref="postOperationRef"/>
            </div>
          </el-tab-pane>


          <el-tab-pane name='assertController' class="h100">
            <template #label>
              <div style="align-items: center; display: flex; justify-content: center">
                <strong>断言规则</strong>
                <div class="el-step__icon is-text zh-header" v-show="getDataLength('validators')">
                  <div class="el-step__icon-inner">{{ getDataLength('validators') }}</div>
                </div>
              </div>
            </template>
            <div class="case-tabs">
              <validators ref="validatorsRef"/>
            </div>
          </el-tab-pane>

        </el-tabs>
      </div>

      <h3 class="block-title">响应内容</h3>
<!--      <report-detail v-if="showTestReportDialog" :data="reportContent"></report-detail>-->

    </div>

    <el-dialog
        draggable
        v-model="showTestReportDialog"
        width="80%"
        top="8vh"
        destroy-on-close
        :close-on-click-modal="false">
      <api-report :reportBody="reportBody"/>
    </el-dialog>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue'
import Url from '/@/views/api/apiCase/components/url.vue'
import Messages from '/@/views/api/apiCase/components/messages.vue'
import RequestBody from '/@/views/api/apiCase/components/requestBody.vue'
import requestHeaders from '/@/views/api/apiCase/components/headers.vue'
import Variables from '/@/views/api/apiCase/components/variables.vue'
import preOperation from "/@/views/api/apiCase/components/preOperation.vue"
import postOperation from "/@/views/api/apiCase/components/postOperation.vue";
import validators from "/@/views/api/apiCase/components/validators.vue";
import {useStore} from "/@/store"
import {useRoute, useRouter} from "vue-router"
import {useApiCaseApi} from '/@/api/useAutoApi/apiCase'
import {ElMessage, ElLoading} from 'element-plus'
import {handleEmpty} from "/@/utils/other";
import apiReport from "/@/views/api/Report/components/report.vue";

export default defineComponent({
  name: 'saveOrUpdateTestCase',
  components: {
    Url,
    Messages,
    RequestBody,
    requestHeaders,
    Variables,
    preOperation,
    postOperation,
    validators,
    apiReport,
  },
  props: {
    case_id: Number
  },
  setup(props) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const urlRef = ref()
    const messagesRef = ref()
    const requestBodyRef = ref()
    const headersRef = ref()
    const preOperationRef = ref()
    const postOperationRef = ref()
    const variablesRef = ref()
    const validatorsRef = ref()
    const state = reactive({
      isShowDialog: false,
      activeName: 'requestBody',
      editType: '',

      // report
      showTestReportDialog: false,
      reportContent: [],

      case_id: null,
    });


    const saveOrUpdateOrDebug = (type: string) => {
      try {
        let urlData = urlRef.value.getData()   // url表单信息
        let messagesData = messagesRef.value.getData()
        let bodyData = requestBodyRef.value.getData()
        let headerData = headersRef.value.getData()
        let preData = preOperationRef.value.getData()
        let postData = postOperationRef.value.getData()
        let variableData = variablesRef.value.getData()
        let validatorsData = validatorsRef.value.getData()

        // 组装表单
        let apiCaseData = {
          id: state.case_id,
          name: messagesData.name,
          project_id: messagesData.project_id,
          module_id: messagesData.module_id,
          code_id: messagesData.code_id,
          code: messagesData.code,
          priority: messagesData.priority,
          method: urlData.method,
          url: urlData.url,
          headers: headerData,
          request_body: bodyData,
          variables: variableData,
          setup_hooks: preData,
          teardown_hooks: postData,
          validators: validatorsData,
        }

        // 保存用例
        if (type === 'save') {
          useApiCaseApi().saveOrUpdate(apiCaseData)
              .then(res => {
                ElMessage.success('保存成功！')
                let case_id = res.data
                state.case_id = case_id
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
          useApiCaseApi().debugTestCaseNew(apiCaseData)
              .then(res => {
                state.reportContent = res.data?.step_datas[0].data
                if (type === 'debug') {
                  console.log('-----------------debug---------------')
                  // urlRef.value.onOpenCloseEnvDialog()
                  // state.reportContent = res.data
                  state.showTestReportDialog = true
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
      let case_id = route.query.id || props.case_id
      if (case_id) {
        state.case_id = case_id
        useApiCaseApi().getTestCaseInfo({id: state.case_id})
            .then(res => {
              let apiCaseData = res.data
              // url
              let urlData = {
                id: apiCaseData.id,
                url: apiCaseData.url,
                method: apiCaseData.method,
              }
              urlRef.value.setData(urlData)

              // 编辑赋值调用 详情
              let messagesData = {
                name: apiCaseData.name,
                code_id: apiCaseData.code_id,
                code: apiCaseData.code,
                project_id: apiCaseData.project_id,
                module_id: apiCaseData.module_id,
              }
              messagesRef.value.setData(messagesData)
              // 编辑赋值调用 请求参数
              requestBodyRef.value.setData(apiCaseData.request_body)
              headersRef.value.setData(apiCaseData.headers)
              variablesRef.value.setData(apiCaseData.variables)
              preOperationRef.value.setData(apiCaseData.setup_hooks, state.case_id)
              postOperationRef.value.setData(apiCaseData.teardown_hooks, state.case_id)
              validatorsRef.value.setData(apiCaseData.validators)

            })
      }
    }

    // 返回到列表
    const goBack = () => {
      router.push({name: 'apiTestCase'})
    }

    // updateHeader
    const getDataLength = (ref: string) => {
      switch (ref) {
        case "header":
          return handleEmpty(headersRef.value.headers).length
        case "variables":
          return handleEmpty(variablesRef.value.variables).length
        case "pre":
          return handleEmpty(preOperationRef.value.teardown_hooks).length
        case "post":
          return handleEmpty(postOperationRef.value.setup_hooks).length
        case "validators":
          return handleEmpty(validatorsRef.value.validators).length
      }
    }

    const updateHeader = (headerData: any, remove: any) => {
      headersRef.value.updateHeader(headerData, remove)
    }

    // 获取是否填写参数状态
    const getStatus = (components: string) => {
      switch (components) {
        case 'body':
          return requestBodyRef.value.getStatus()
        case 'vp':
          return variablesRef.value.getStatus()
        case 'ev':
          // return extractValidateRef.value.getStatus()
      }
    }

    onMounted(() => {
      initTestCase()
    })

    return {
      urlRef,
      messagesRef,
      requestBodyRef,
      headersRef,
      variablesRef,
      preOperationRef,
      postOperationRef,
      validatorsRef,
      store,
      route,
      router,
      goBack,
      getDataLength,
      updateHeader,
      saveOrUpdateOrDebug,
      getStatus,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
.block-title {
  position: relative;
  margin-bottom: 12px;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 28px;
  line-height: 28px;
  background: #f7f7fc;
  color: #333333;

  &::before {
    content: '';
    position: absolute;
    top: 7px;
    left: 0;
    width: 3px;
    height: 14px;
    background: #409eff;
  }
}

:deep(.page-header .el-page-header__icon .el-icon) {
  background-color: #3883fa;
  border-radius: 50%;
  color: white;
}

:deep(.el-page-header .page-header) {
  margin-left: 0 !important;
}
:deep(.el-page-header__breadcrumb) {
  margin-bottom: 0;
}
//:deep(.save-update-card .el-card__body) {
//  padding-top: 0;
//}
.save-update-card {
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  background-color: #ffffff;
  overflow-x: hidden;
  overflow-y: auto;
  color: #303133;
  transition: 0.3s;
  padding: 10px;
}

:deep(.el-tabs__header) {
  margin: 0 0 10px;
}

:deep(.el-tabs__item.is-active) {
  color: var(--el-text-color-primary);
}

//:deep(.el-tabs__item:hover) {
//  color: var(--el-text-color-primary);
//}

.request-editor-tabs-badge {
  background-color: #61affe;
  display: inline-flex;
  width: 8px;
  height: 8px;
  margin-left: 5px;
  border-radius: 8px;
}

.case-tabs {
  border: 1px solid #E6E6E6;
  padding: 8px;
  border-radius: 5px;
}

.zh-header {
  background: #61affe;
  color: #fff;
  height: 18px;
  font-size: xx-small;
  border-radius: 50%;
}

</style>