<template>
  <div class="el-card">
    <el-page-header
        class="page-header"
        style="margin: 5px 0;"
        @back="goBack"
    >
      <template #content>
        <span style="padding-right: 10px;">{{ editType === 'save' ? '新增套件' : '更新套件' }}</span>
      </template>
      <template #extra>
        <el-button type="success" @click="debugSuite">调试</el-button>
        <el-button type="primary" @click="saveOrUpdate" class="title-button">保存</el-button>
      </template>
    </el-page-header>

    <el-divider style="margin: 10px 0 5px 0;"/>

    <div class="el-card" style="height: calc(100% - 50.50px);">
      <splitpanes class="default-theme" style="height: 100%;">
        <pane :size="20">
          <div style="padding: 0 10px 0 0">

            <el-form
                ref="formRef"
                :model="form"
                :rules="rules"
                label-position="right"
                label-width="80px"
                size="small"
                status-icon
            >
              <el-form-item label="套件名称：" prop="name">
                <el-input v-model="form.name" placeholder="套件名称"></el-input>
              </el-form-item>

              <el-form-item label="所属项目：" prop="project_id">
                <el-select size="small"
                           v-model="form.project_id"
                           placeholder="选择所属项目"
                           filterable
                           style="width: 100%;"
                >
                  <el-option
                      v-for="project in projectList"
                      :key="project.id"
                      :label="project.name"
                      :value="project.id">
                    <span style="float: left">{{ project.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>


              <el-form-item label="运行环境：" prop="env_id">
                <el-select size="small"
                           v-model="form.env_id"
                           placeholder="运行环境"
                           filterable
                           style="width: 100%;"
                >
                  <el-option
                      v-for="env in envList"
                      :key="env.id + env.name"
                      :label="env.name"
                      :value="env.id">
                    <span style="float: left">{{ env.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="步骤总数：">
                {{ form.step_data?.length }}
              </el-form-item>

              <el-form-item label="套件变量：">
                <el-link type="info" @click="isShowVariable = ! isShowVariable">
                  {{ handleEmpty(form.headers).length + handleEmpty(form.variables).length }}
                </el-link>
              </el-form-item>

            </el-form>

          </div>
        </pane>
        <pane :size="80" :min-size="50">
          <step-controller
              ref="stepControllerRef"
              use_type="suite"
              style="margin-bottom: 10px"
              v-model:data="form.step_data"></step-controller>
        </pane>
      </splitpanes>

    </div>


    <el-dialog
        draggable
        title="变量" v-model="isShowVariable" width="769px"
    >
      <el-tabs v-model="activeTabName" class="demo-tabs">
        <el-tab-pane label="变量" name="variable">
          <template #label>
            <strong>变量
              <div class="el-step__icon is-text zh-header" v-show="handleEmpty(form.variables).length">
                <div class="el-step__icon-inner">{{ handleEmpty(form.variables).length }}</div>
              </div>
            </strong>
          </template>
          <variable-controller :data="form.variables"></variable-controller>
        </el-tab-pane>
        <el-tab-pane label="请求头" name="second">
          <template #label>
            <strong>请求头
              <div class="el-step__icon is-text zh-header" v-show="handleEmpty(form.headers).length">
                <div class="el-step__icon-inner">{{ handleEmpty(form.headers).length }}</div>
              </div>
            </strong>
          </template>
          <headers-controller :data="form.headers"></headers-controller>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue';
import {ElMessage} from "element-plus";
import {useApiSuiteApi} from "/@/api/useAutoApi/apiSuite";
import {useRoute, useRouter} from "vue-router"
import {useEnvApi} from "/@/api/useAutoApi/env";
import variableController from "/@/components/StepController/variable/variableController.vue";
import headersController from "/@/components/StepController/headers/headersController.vue";
import {useProjectApi} from "/@/api/useAutoApi/project";
import {Pane, Splitpanes} from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';
import {handleEmpty} from "/@/utils/other";


export default defineComponent({
  name: 'saveOrUpdateSuite',
  components: {
    variableController,
    headersController,
    Splitpanes,
    Pane,
  },
  setup() {
    const createForm = () => {
      return {
        name: '', // 名称
        env_id: null, // 环境id
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
      // 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式
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
    const initData = () => {
      if (route.query.id) {
        useApiSuiteApi().getSuitesInfo({id: route.query.id}).then(res => {
          state.form = res.data
        })
      }
    }

    // environment
    const getEnvList = () => {
      useEnvApi().getList({page: 1, pageSize: 100})
          .then(res => {
            state.envList = res.data.rows
          })
    };

    // project
    // 初始化表格数据
    const getProjectList = () => {
      useProjectApi().getList({page: 1, pageSize: 1000})
          .then(res => {
            state.projectList = res.data.rows
          })
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

      useApiSuiteApi().saveOrUpdate(state.form)
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
          useApiSuiteApi().debugSuites(state.form)
              .then((res: any) => {
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
      router.push({name: 'apiCaseSuite'})
    }
    // 页面加载时
    onMounted(() => {
      initData()
      getEnvList()
      getProjectList()
    });

    return {
      formRef,
      initData,
      saveOrUpdate,
      debugSuite,
      goBack,
      route,
      router,
      handleEmpty,
      stepControllerRef,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

.block-title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 20px;
  line-height: 20px;
  background: #f7f7fc;
  color: #333333;
  border-left: 2px solid #409eff;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

.el-card {
  padding: 10px;
}

:deep(.el-page-header__breadcrumb) {
  display: none;
}

.splitpanes.default-theme .splitpanes__pane {
  background-color: #ffffff;
}

.zh-header {
  background: #61affe;
  color: #fff;
  height: 18px;
  font-size: xx-small;
  border-radius: 50%;
}
</style>