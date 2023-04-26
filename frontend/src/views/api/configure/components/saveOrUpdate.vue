<template>
  <div class="system-edit-menu-container">
    <el-card class="save-update-card">
      <div>
        <!--        <el-page-header-->
        <!--            class="page-header"-->
        <!--            :content="editType === 'create'? '新增配置':'更新配置'"-->
        <!--            style="margin: 10px 0;"-->
        <!--            @back="goBack"-->
        <!--        >-->
        <!--        </el-page-header>-->

        <!--        <h3 class="block-title">请求信息</h3>-->

        <!--        <url ref="urlRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>-->

        <h3 class="block-title">基本信息</h3>

        <messages ref="messagesRef"/>

        <h3 class="block-title">参数信息</h3>
        <div style="min-height: 500px">
          <el-tabs v-model="activeName">
            <!--            <el-tab-pane name='requestBody'>-->
            <!--              <template #label><strong>body</strong></template>-->
            <!--              <request-body ref="requestBodyRef"/>-->
            <!--            </el-tab-pane>-->

            <el-tab-pane name='requestHeaders'>
              <template #label><strong>Headers</strong></template>
              <request-headers ref="requestHeadersRef"/>
            </el-tab-pane>

            <!--            <el-tab-pane name='extractValidate'>-->
            <!--              <template #label><strong>提取/校验</strong></template>-->
            <!--              <extract-validate ref="extractValidateRef"/>-->
            <!--            </el-tab-pane>-->

            <el-tab-pane name='variablesParameters'>
              <template #label><strong>变量/参数/函数</strong></template>
              <variables-parameters ref="variablesParametersRef"/>
            </el-tab-pane>

          </el-tabs>
        </div>
      </div>
    </el-card>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue'
import Messages from '/@/views/api/configure/components/messages.vue'
import RequestHeaders from '/@/views/api/configure/components/requestHeaders.vue'
// import ExtractValidate from '/@/views/api/configure/components/ExtractValidate.vue'
import VariablesParameters from '/@/views/api/configure/components/variablesParameters.vue'
import {ElMessage} from "element-plus"
import {useRoute, useRouter} from "vue-router"
import {useTestCaseApi} from '/@/api/useAutoApi/testCase'

export default defineComponent({
  name: 'saveOrUpdateConfigure',
  components: {
    Messages,
    RequestHeaders,
    // ExtractValidate,
    VariablesParameters,
  },
  props: {
    config_id: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const userInfo = store.state.userInfos
    const messagesRef = ref()
    const requestHeadersRef = ref()
    // const extractValidateRef = ref()
    const variablesParametersRef = ref()
    const state = reactive({
      isShowDialog: false,
      activeName: 'requestHeaders',

    });


    const saveOrUpdate = () => {
      try {
        // 获取url mothod 表单
        let msgForm = messagesRef.value.getFormData()
        let headForm = requestHeadersRef.value.getFormData()
        let bodyForm = {headers: headForm}
        // let EVForm = extractValidateRef.value.getFormData()
        let VPForm = variablesParametersRef.value.getFormData()
        // let skipForm = skipRef.value.getFormData()

        // 组装表单
        let testCaseForm = {
          id: msgForm.id,
          user_id: userInfo.userInfos.id,
          name: msgForm.name,
          case_type: 2,
          project_id: msgForm.project_id,
          module_id: msgForm.module_id,
          run_type: 1,
          testcase: {
            // skip: true,
            case_id: msgForm.id,
            request: bodyForm,
            name: msgForm.name,
            parameters: VPForm.parameters,
            variables: VPForm.variables,
            // hooks: VPForm.hooks,
            // setup_hooks: VPForm.setup_hooks,
            // teardown_hooks: VPForm.teardown_hooks,
            // extract: EVForm.extract,
            // validate: EVForm.validate,
          },
        }
        // 保存用例
        useTestCaseApi().saveOrUpdate(testCaseForm).then(res => {
          ElMessage.success('保存成功！')
          let case_id = res.data
          messagesRef.value.setCaseId(case_id)
        })
      } catch (err: any) {
        console.log(err)
        ElMessage.info(err || '信息表单填写不完整')

      }
    }

    const initTestCast = () => {
      if (props.config_id) {
        useTestCaseApi().getTestCaseInfo({id: props.config_id, case_type: 2}).then(res => {
          let data = res.data
          let case_data = data.testcase

          // msg
          let case_info = {
            id: data.id,
            name: data.name,
            module_id: data.module_id,
            project_id: data.project_id,
            run_type: data.run_type,
            user_id: data.user_id,
          }
          // case_info.id = c_id
          // 编辑赋值调用 详情
          messagesRef.value.initForm(case_info)
          // 编辑赋值调用 请求参数
          // requestBodyRef.value.initForm(case_data.request)
          requestHeadersRef.value.initForm(case_data.request)
          // extractValidate
          // let evForm = {
          //   extract: case_data.extract,
          //   validate: case_data.validate,
          // }
          // extractValidateRef.value.initForm(evForm)

          //variablesParameters
          let vpFrom = {
            variables: case_data.variables,
            parameters: case_data.parameters,
            setup_hooks: case_data.setup_hooks,
            teardown_hooks: case_data.teardown_hooks,
            // hooks: case_data.hooks,
          }
          variablesParametersRef.value.initForm(vpFrom)
          // outputListRef.value.initForm(case_data.output)
          // if (case_data.skip_info) {
          //   skipRef.value.initForm(case_data.skip_info)
          // }
        })
      }
    }

    // 返回到列表
    const goBack = () => {
      router.push({name: 'apiTestCase'})
    }

    onMounted(() => {
      initTestCast()
    })

    return {
      messagesRef,
      requestHeadersRef,
      // extractValidateRef,
      variablesParametersRef,
      store,
      route,
      router,
      goBack,
      saveOrUpdate,
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

:deep(.save-update-card .el-card__body) {
  padding-top: 0;
}
</style>