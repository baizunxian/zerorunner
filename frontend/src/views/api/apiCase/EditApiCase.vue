<template>
  <div class="app-container h100">
    <el-card class="step-content" style="height: 100%;" :body-style="{height: 'calc(100% - 66.5px)'}">
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
            <el-dropdown :hide-on-click="false" class="pr12">
              <el-button type="warning">
                添加步骤
                <el-icon class="el-icon--right">
                  <arrowDown/>
                </el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-for="(value, key)  in state.optTypes"
                                    :key="key"
                                    style="margin: 5px 0"
                                    :style="{ color: getStepTypeInfo(key,'color')}"
                                    @click="handleAddData(key)">
                    <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"
                       :style="{color:getStepTypeInfo(key,'color')}"></i>
                    {{ value }}
                  </el-dropdown-item>

                </el-dropdown-menu>
              </template>
            </el-dropdown>

            <el-button type="success" @click="openRunPage">调试</el-button>
            <el-button type="primary" @click="saveOrUpdate" class="title-button">保存</el-button>
          </template>
        </z-detail-page-header>
      </template>


      <z-splitpanes class="default-theme h100">
        <z-pane :size="25">
          <div style="padding: 0 10px 0 0">

            <el-form
                ref="formRef"
                :model="state.form"
                :rules="state.rules"
                label-position="right"
                label-width="auto"
                size="small"
            >
              <el-form-item label="用例名称：" prop="name">
                <el-input v-model="state.form.name" placeholder="用例名称" clearable></el-input>
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
                  <el-radio :label="1" size="small" border>是
                    <el-tooltip content="用例顺序执行，上个用例提取的用例后面的用例都能使用" placement="top">
                      <el-icon class="statistics-comparison__text">
                        <ele-InfoFilled></ele-InfoFilled>
                      </el-icon>
                    </el-tooltip>
                  </el-radio>

                  <el-radio :label="0" size="small" border>否
                    <el-tooltip content="用例随机执行，并且上个用例提取的结果后面的用例获取不到" placement="top">
                      <el-icon class="statistics-comparison__text">
                        <ele-InfoFilled></ele-InfoFilled>
                      </el-icon>
                    </el-tooltip>
                  </el-radio>
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
          <!--          <nestedDraggable v-if="state.step_data" :List="state.step_data"></nestedDraggable>-->
          <z-step-controller
              ref="stepControllerRef"
              use_type="case"
              style="margin-bottom: 10px"
              v-model:steps="state.form.step_data">
          </z-step-controller>
        </z-pane>
      </z-splitpanes>


      <el-dialog
          draggable
          title="用例变量" v-model="state.isShowVariable" width="769px"
      >
        <el-tabs v-model="state.activeTabName" class="demo-tabs">
          <el-tab-pane label="变量" name="variable">
            <template #label>
              <strong>变量</strong>
              <span class="ui-badge-circle" v-show="getDataLength('variables')">{{ getDataLength('variables') }}</span>
            </template>
            <VariableController :data="state.form.variables"></VariableController>
          </el-tab-pane>
          <el-tab-pane label="请求头" name="second">
            <template #label>
              <strong>请求头</strong>
              <span class="ui-badge-circle" v-show="getDataLength('headers')">{{ getDataLength('headers') }}</span>
            </template>
            <HeadersController v-model:data="state.form.headers"></HeadersController>
          </el-tab-pane>
        </el-tabs>
      </el-dialog>
    </el-card>

    <el-dialog
        draggable
        v-if="state.showReportDialog"
        v-model="state.showReportDialog"
        width="90%"
        top="5vh"
        destroy-on-close
        :close-on-click-modal="false">
      <template #header>
        <strong>报告详情</strong>
        <!--      <el-button class="ml5" style="font-size: 12px" type="primary" link @click="state.showLog=!state.showLog">-->
        <!--        执行日志-->
        <!--      </el-button>-->
      </template>

      <ReportDetail :report-info="state.reportInfo" :is-debug="true" ref="reportDetailRef"/>

    </el-dialog>

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

<script setup name="EditApiCase">
import {onActivated, onMounted, reactive, ref, watch} from 'vue';
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
import {getStepTypeInfo, getStepTypesByUse} from "/@/utils/case";
import {ArrowDown} from "@element-plus/icons";

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
  showReportDialog: false,
  reportInfo: null,
//  showRunPage
  showRunPage: false,
  optTypes: getStepTypesByUse("case")
});

// init suite
const initData = async () => {
  if (route.query.id) {
    let {data} = await useApiCaseApi().getCaseInfo({id: route.query.id})
    state.form = data
  } else {
    state.form = createForm()
  }
}

const handleStepData = (step_data) => {
  step_data.forEach((e) => {
    if (e.sub_steps) {
      handleStepData(e.sub_steps)
    } else {
      e.sub_steps = []
    }
  })
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

// 新增修改
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
      .then((res) => {
        state.form.id = res.data.id
        state.form.version = res.data.version
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
  formRef.value.validate((valid) => {
    if (valid) {
      if (state.form.step_data.length === 0) {
        ElMessage.warning("请先添加步骤！")
        return
      }
      state.runCaseLoading = true
      state.form.variables = handleEmpty(state.form.variables)
      state.form.headers = handleEmpty(state.form.headers)
      useApiCaseApi().debugSuites(state.form)
          .then((req) => {
            state.reportInfo = req.data
            state.showReportDialog = !state.showReportDialog
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

const getDataLength = (dataType) => {
  if (dataType === "headers") {
    return handleEmpty(state.form.headers).length
  }
  if (dataType === "variables") {
    return handleEmpty(state.form.variables).length
  }
}

//handleAddData
const handleAddData = (optType) => {
  stepControllerRef.value.handleAddData(optType)

}

// goBack
const goBack = () => {
  router.push({name: 'apiCase'})
}

onActivated(() => {
  if (state.timestamp !== route.query.timestamp) {
    state.timestamp = route.query.timestamp
    initData()
  }
})

// 页面加载时
onMounted(() => {
  initData()
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
  top: 10px;
  right: calc(-7px + var(--el-badge-size) / 2);
}

:deep(.el-dropdown) {
  vertical-align: middle;
}
</style>