<template>
  <div class="system-edit-menu-container h100">
    <el-page-header
        class="page-header"
        style="margin: 10px 0;"
        @back="goBack"
    >
      <template #content>
        <span style="padding-right: 10px;">{{ editType === 'save' ? '新增套件' : '更新套件' }}</span>
        <!--        <el-button type="primary" @click="saveOrUpdate" class="title-button">保存</el-button>-->
      </template>
    </el-page-header>
    <h3 class="block-title">基本信息</h3>
    <el-card>
      <div>
        <el-row :span="24">
          <el-col :span="3">
             <el-input
                v-model="form.name"
                placeholder="套件名称"
            >
             </el-input>
          </el-col>
          <el-col :span="3">步骤总数:{{ form.step_data?.length }}</el-col>
          <el-col :span="3">
            <el-link type="info" @click="isShowVariable = ! isShowVariable">套件变量</el-link>
          </el-col>
          <el-col :span="4">
            <div style="display: flex">
              <div style="width: 80px">所属项目</div>
              <el-select size="small" v-model="form.project_id" placeholder="选择所属项目" filterable
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
            </div>

          </el-col>
          <el-col :span="4">
            <div style="display: flex">
              <div style="width: 80px">运行环境</div>
              <el-select size="small" v-model="form.env_id" placeholder="运行环境" filterable
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
            </div>

          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="debugSuite" class="title-button">调试</el-button>
            <el-button type="primary" @click="saveOrUpdate" class="title-button">保存</el-button>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <div style="padding-top: 8px">
      <step-controller step_type="suite" :data="form.step_data"></step-controller>
    </div>

    <el-dialog
        draggable
        title="变量" v-model="isShowVariable" width="769px"
    >
      <el-tabs v-model="activeTabName" class="demo-tabs">
        <el-tab-pane label="变量" name="variable">
          <variable-controller :data="form.variables"></variable-controller>
        </el-tab-pane>
        <el-tab-pane label="请求头" name="second">
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
import variableController from "/@/components/StepController/variableController.vue";
import headersController from "/@/components/StepController/headersController.vue";
import {useProjectApi} from "/@/api/useAutoApi/project";


export default defineComponent({
  name: 'saveOrUpdateSuite',
  components: {
    variableController,
    headersController,
  },
  setup(props, {emit}) {
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
    const route = useRoute()
    const router = useRouter()
    const state = reactive({
      isShowVariable: false,
      editType: '',
      // 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式
      form: createForm(),
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
      useProjectApi().getList({page:1, pageSize: 1000})
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
       useApiSuiteApi().debugSuites(state.form)
          .then((res:any) => {
            ElMessage.success('操作成功');
          })
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
      initData,
      saveOrUpdate,
      debugSuite,
      goBack,
      route,
      router,
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

:deep(.el-c) {

}
</style>