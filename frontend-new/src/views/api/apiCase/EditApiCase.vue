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
            <span style="padding-right: 10px;">{{ state.editType === 'save' ? '新增套件' : '更新套件' }}</span>
          </template>

          <template #extra>
            <el-button type="success" @click="debugSuite">调试</el-button>
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
              <el-form-item label="套件名称：" prop="name">
                <el-input v-model="state.form.name" placeholder="套件名称"></el-input>
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


              <el-form-item label="运行环境：" prop="env_id">
                <el-select size="small"
                           v-model="state.form.env_id"
                           placeholder="运行环境"
                           filterable
                           style="width: 100%;"
                >
                  <el-option
                      v-for="env in state.envList"
                      :key="env.id + env.name"
                      :label="env.name"
                      :value="env.id">
                    <span style="float: left">{{ env.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="步骤依赖：">
                <el-radio-group v-model="state.form.step_rely">
                  <el-radio :label="true" size="small">是</el-radio>
                  <el-radio :label="false" size="small">否</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="步骤总数：">
                {{ state.form.step_data?.length }}
              </el-form-item>

              <el-form-item label="套件变量：">
                <template #label>
                  <el-link type="primary" @click="state.isShowVariable = ! state.isShowVariable">套件变量：</el-link>
                </template>
                <el-link type="info" @click="state.isShowVariable = ! state.isShowVariable">
                  {{ handleEmpty(state.form.headers).length + handleEmpty(state.form.variables).length }}
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
          title="变量" v-model="state.isShowVariable" width="769px"
      >
        <el-tabs v-model="state.activeTabName" class="demo-tabs">
          <el-tab-pane label="变量" name="variable">
            <template #label>
              <el-badge :hidden="!handleEmpty(state.form.variables).length"
                        :value="handleEmpty(state.form.variables).length"
                        class="badge-item"
                        type="primary">
                <strong>变量</strong>
              </el-badge>
            </template>
            <VariableController :data="state.form.variables"></VariableController>
          </el-tab-pane>
          <el-tab-pane label="请求头" name="second">
            <template #label>
              <el-badge :hidden="!handleEmpty(state.form.variables).length"
                        :value="handleEmpty(state.form.variables).length"
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

const createForm = () => {
  return {
    name: '', // 名称
    env_id: null, // 环境id
    step_rely: true, // 步骤依赖
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
const state = reactive({
  isShowVariable: false,
  editType: '',
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
    project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'}],
    env_id: [{required: true, message: '请选择运行环境', trigger: 'blur'}],
  },
  // project
  projectList: [],
  // environment
  envList: [],
  // tabs
  activeTabName: "variable",
});

// init suite
const initData = async () => {
  if (route.query.id) {
    let {data} = await useApiCaseApi().getSuitesInfo({id: route.query.id})
    state.form = data
  }
}

// environment
const getEnvList = async () => {
  let {data} = await useEnvApi().getList({page: 1, pageSize: 100})
  state.envList = data.rows
};

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
  if (!state.form.env_id) {
    ElMessage.warning('请选择对应运行环境！');
    return
  }
  if (state.form?.step_data.length === 0) {
    ElMessage.warning('请添加步骤！');
    return
  }

  useApiCaseApi().saveOrUpdate(state.form)
      .then(() => {
        ElMessage.success('操作成功');
      })
};

// debugSuite
const debugSuite = () => {
  formRef.value.validate((valid: any) => {
    if (valid) {
      if (state.form.step_data.length == 0) {
        ElMessage.warning("请先添加步骤！")
        return
      }
      useApiCaseApi().debugSuites(state.form)
          .then(() => {
            ElMessage.success('操作成功');
          })
    } else {
      ElMessage.warning("必填信息不能为空！")
    }

  })

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
  getEnvList()
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