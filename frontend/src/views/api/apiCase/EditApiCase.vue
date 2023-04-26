<template>
  <div class="app-container h100">
    <el-card class="step-content" style="height: 100%;">
      <template #header>
        <z-detail-page-header
            class="page-header"
            style="margin: 5px 0;"
            @back="goBack"
        >
          <template #content>
            <span style="padding-right: 10px;">{{ state.editType === 'save' ? '新增用例' : '更新用例' }}</span>
          </template>

          <template #extra>
            <el-button type="success" @click="openRunPage">调试</el-button>
            <el-button type="primary" @click="saveOrUpdate" class="title-button">保存</el-button>
          </template>
        </z-detail-page-header>
      </template>


      <z-splitpanes class="default-theme h100">
        <z-pane :size="20">
          <div style="padding: 0 10px 0 0">

            <el-form
                ref="formRef"
                :model="state.form"
                :rules="state.rules"
                label-position="right"
                label-width="auto"
                size="small"
                status-icon
            >
              <el-form-item label="用例名称：" prop="name">
                <el-input v-model="state.form.name" placeholder="用例名称"></el-input>
              </el-form-item>

              <el-form-item label="所属项目：" prop="project_id">
                <el-select size="small"
                           v-model="state.form.project_id"
                           placeholder="选择所属项目"
                           filterable
                           style="width: 100%;"
                >
                  <el-option
                      v-for="project in state.projectList"
                      :key="project.id"
                      :label="project.name"
                      :value="project.id">
                    <span style="float: left">{{ project.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>


              <!--              <el-form-item label="运行环境：" prop="env_id">-->
              <!--                <el-select size="small"-->
              <!--                           v-model="state.form.env_id"-->
              <!--                           placeholder="运行环境"-->
              <!--                           filterable-->
              <!--                           style="width: 100%;"-->
              <!--                >-->
              <!--                  <el-option-->
              <!--                      v-for="env in state.envList"-->
              <!--                      :key="env.id + env.name"-->
              <!--                      :label="env.name"-->
              <!--                      :value="env.id">-->
              <!--                    <span style="float: left">{{ env.name }}</span>-->
              <!--                  </el-option>-->
              <!--                </el-select>-->
              <!--              </el-form-item>-->

              <el-form-item label="用例描述：" prop="remarks">
                <el-input v-model="state.form.remarks"></el-input>
              </el-form-item>

              <el-form-item label="步骤依赖：">
                <el-radio-group v-model="state.form.step_rely">
                  <el-radio :label="1" size="small" border>是</el-radio>
                  <el-radio :label="0" size="small" border>否</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="步骤总数：">
                {{ state.form.step_data?.length }}
              </el-form-item>

              <el-form-item label="用例变量：">
                <template #label>
                  <el-link type="primary" @click="state.isShowVariable = ! state.isShowVariable">用例变量：</el-link>
                </template>
                <el-link type="info" @click="state.isShowVariable = ! state.isShowVariable">
                  {{ getDataLength('headers') + getDataLength('variables') }}
                </el-link>
              </el-form-item>

            </el-form>

          </div>
        </z-pane>
        <z-pane :size="80" :min-size="50">
          <!--          <apiInfo-step></apiInfo-step>-->
          <z-step-controller
              ref="stepControllerRef"
              use_type="suite"
              style="margin-bottom: 10px"
              v-model:data="state.form.step_data"></z-step-controller>
        </z-pane>
      </z-splitpanes>


      <el-dialog
          draggable
          title="用例变量" v-model="state.isShowVariable" width="769px"
      >
        <el-tabs v-model="state.activeTabName" class="demo-tabs">
          <el-tab-pane label="变量" name="variable">
            <template #label>
              <el-badge :hidden="!getDataLength('variables')"
                        :value="getDataLength('variables')"
                        class="badge-item"
                        type="primary">
                <strong>变量</strong>
              </el-badge>
            </template>
            <VariableController :data="state.form.variables"></VariableController>
          </el-tab-pane>
          <el-tab-pane label="请求头" name="second">
            <template #label>
              <el-badge :hidden="!getDataLength('headers')"
                        :value="getDataLength('headers')"
                        class="badge-item"
                        type="primary">
                <strong>请求头</strong>
              </el-badge>
            </template>
            <HeadersController :data="state.form.headers"></HeadersController>
          </el-tab-pane>
        </el-tabs>
      </el-dialog>
    </el-card>
    <ReportDetail ref="ReportDetailRef" :report-info="state.reportInfo" :is-debug="true"></ReportDetail>

    <el-dialog
        draggable
        v-model="state.showRunPage"
        width="600px"
        top="8vh"
        title="运行用例"
        :close-on-click-modal="false">
      <el-form
          :model="state.form"
          label-width="70px"

      >
        <el-form-item label="运行环境" prop="belong_project_id">
          <el-select v-model="state.form.env_id" placeholder="选择环境" filterable style="width:100%">
            <el-option :value="''" label="自带环境">自带环境</el-option>
            <el-option
                v-for="item in state.envList"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              <span style="float: left">{{ `${item.name}(${item.domain_name})` }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
                <span class="dialog-footer">
                  <el-button @click="state.showRunPage = !state.showRunPage">取消</el-button>
                  <el-button type="primary" :loading="state.runCaseLoading" @click="debugApiCase">运行</el-button>
                </span>
      </template>
    </el-dialog>

  </div>
</template>

<script lang="ts" setup name="EditApiCase">
import {onMounted, reactive, ref} from 'vue';
import {ElMessage} from "element-plus";
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";
import {useRoute, useRouter} from "vue-router"
import {useEnvApi} from "/@/api/useAutoApi/env";
import VariableController from "/@/components/Z-StepController/variable/VariableController.vue";
import HeadersController from "/@/components/Z-StepController/headers/HeadersController.vue";
import {useProjectApi} from "/@/api/useAutoApi/project";
import 'splitpanes/dist/splitpanes.css';
import {handleEmpty} from "/@/utils/other";
import ReportDetail from "/@/components/Z-Report/ApiReport/ReportInfo/ReportDetail.vue"

const createForm = () => {
  return {
    name: '', // 名称
    env_id: null, // 环境id
    step_rely: 1, // 步骤依赖
    project_id: '', // 关联项目
    remarks: '', // 简要描述
    step_data: [],
    variables: [],
    headers: [],
  }
}
const stepControllerRef = ref()
const formRef = ref()
const route = useRoute()
const router = useRouter()
const ReportDetailRef = ref()
const state = reactive({
  isShowVariable: false,
  editType: '',
  form: createForm(),
  runCaseLoading: false, // 运行loading
  rules: {
    name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
    project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'}],
    // env_id: [{required: true, message: '请选择运行环境', trigger: 'blur'}],
  },
  // project
  projectList: [],
  // environment
  envList: [],
  // tabs
  activeTabName: "variable",
//  report
  reportInfo: null,
//  showRunPage
  showRunPage: false
});

// init suite
const initData = async () => {
  if (route.query.id) {
    let {data} = await useApiCaseApi().getCaseInfo({id: route.query.id})
    state.form = data
  }
}

// environment
// const getEnvList = async () => {
//   let {data} = await useEnvApi().getList({page: 1, pageSize: 100})
//   state.envList = data.rows
// };

// project
// 初始化表格数据
const getProjectList = async () => {
  let {data} = await useProjectApi().getList({page: 1, pageSize: 1000})
  state.projectList = data.rows

};

// 新增
const saveOrUpdate = () => {
  if (!state.form.project_id) {
    ElMessage.warning('请选择所属项目！');
    return
  }
  // if (!state.form.env_id) {
  //   ElMessage.warning('请选择对应运行环境！');
  //   return
  // }
  if (state.form?.step_data.length === 0) {
    ElMessage.warning('请添加步骤！');
    return
  }
  state.form.variables = handleEmpty(state.form.variables)
  state.form.headers = handleEmpty(state.form.headers)
  useApiCaseApi().saveOrUpdate(state.form)
      .then(() => {
        ElMessage.success('操作成功');
      })
};
// openRunPage
const openRunPage = () => {
  state.showRunPage = true
  getEnvList()
}

// 获取环境信息
const getEnvList = () => {
  useEnvApi().getList({page: 1, pageSize: 1000}) // 请求数据写死，后面优化
      .then(res => {
        state.envList = res.data.rows
      })
};

// debugApiCase
const debugApiCase = () => {
  formRef.value.validate((valid: any) => {
    if (valid) {
      if (state.form.step_data.length == 0) {
        ElMessage.warning("请先添加步骤！")
        return
      }
      state.runCaseLoading = true
      state.form.variables = handleEmpty(state.form.variables)
      state.form.headers = handleEmpty(state.form.headers)
      useApiCaseApi().debugSuites(state.form)
          .then((req: any) => {
            state.reportInfo = req.data
            ReportDetailRef.value.showReport()
            ElMessage.success('操作成功');
            state.runCaseLoading = false
            state.showRunPage = false
          }).catch((err) => {
        console.log(err)
        state.runCaseLoading = false
      })
    } else {
      ElMessage.warning("必填信息不能为空！")
    }

  })

}

const getDataLength = (dataType: string) => {
  if (dataType == "headers") {
    return handleEmpty(state.form.headers).length
  }
  if (dataType == "variables") {
    return handleEmpty(state.form.variables).length
  }
}


// 全局点击事件，取消step 选中
window.onclick = () => {
  stepControllerRef.value?.clickBlank()
  stepControllerRef.value?.initFabMenu(null)
}
// goBack
const goBack = () => {
  router.push({name: 'apiCase'})
}
// 页面加载时
onMounted(() => {
  initData()
  // getEnvList()
  getProjectList()
});

</script>

<style lang="scss" scoped>

.step-content {
  :deep(.el-card__body) {
    height: 100%;
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