<template>
  <el-form ref="formRef" :model="form" label-width="auto" label-position="left"
           :rules="rules">
    <el-row :gutter="24">
      <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb20">
        <el-form-item label="用例名" prop="name">
          <el-input v-model.trim="form.name" style="width: 100%;" placeholder="请输入用例名称"></el-input>
        </el-form-item>
      </el-col>

      <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb20">
        <el-form-item label="所属项目" prop="project_id">
          <el-select size="small" v-model="form.project_id" placeholder="选择所属项目" filterable style="width: 100%;"
                     @change="selectProject">
            <el-option
                v-for="project in projectList"
                :key="project.id + project.name"
                :label="project.name"
                :value="project.id">
              <span style="float: left">{{ project.name }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb20">
        <el-form-item label="可选模块" prop="module_id">
          <el-select size="small" v-model="form.module_id" placeholder="选择模块" filterable style="width: 100%;">
            <el-option
                v-for="modules in moduleList"
                :key="modules.id + modules.name"
                :label="modules.name"
                :value="modules.id">
              <span style="float: left">{{ modules.name }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-col>

      <!--      <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb20">-->
      <!--        <el-form-item label="关联配置" prop="config_id">-->
      <!--          <el-select size="small" v-model="form.config_id" placeholder="请选择配置" clearable filterable-->
      <!--                     style="width: 100%;">-->
      <!--            <el-option-->
      <!--                v-for="item in configList"-->
      <!--                :key="item.id"-->
      <!--                :label="item.name"-->
      <!--                :value="item.id">-->
      <!--                  <span style="float: left">-->
      <!--                    {{ item.name }}-->
      <!--                  </span>-->
      <!--            </el-option>-->
      <!--          </el-select>-->
      <!--        </el-form-item>-->
      <!--      </el-col>-->

    </el-row>
  </el-form>

</template>

<script lang="ts">
import {useProjectApi} from '/@/api/useAutoApi/project'
import {useModuleApi} from '/@/api/useAutoApi/module'
import {defineComponent, onMounted, reactive, ref, toRefs} from "vue";


export default defineComponent({
  name: 'caseMessages',
  components: {},
  setup() {
    const formRef = ref()
    const createForm = () => {
      return {
        name: '',
        code_id: null,
        code: '',
        project_id: null,
        module_id: null,
        priority: 3,
      }
    }
    const state = reactive({
      // cat apiCase info
      showCaseInfo: false,
      // form
      isShowDialog: false,
      handleType: '',   //apiCase 调用类型， 保存，调试
      // 表单及校验
      form: createForm(),
      rules: {
        name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
        project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'}],
        module_id: [{required: true, message: '请选择所属模块', trigger: 'blur'}],
      },
      // project
      projectList: [],
      projectQuery: {
        page: 1,
        pageSize: 1000,
      },
      // module
      moduleList: [],
      moduleQuery: {
        page: 1,
        pageSize: 1000,
        project_id: null,
      },

    });
    // 初始化表单
    const setData = (formData: any) => {
      state.form = createForm()
      if (formData) state.form = formData
      if (formData.project_id) {
        state.moduleQuery.project_id = formData.project_id
        getModuleList()
      }
    }

    // 获取表单数据
    const getData = () => {
      return state.form
    }
    //  ----------------project start-------------------------------------
    // 获取项目列表 请求写死
    const getProjectList = () => {
      useProjectApi().getList(state.projectQuery)
          .then(res => {
            state.projectList = res.data.rows
          })
    }
    // 选择项目
    const selectProject = (project_id: any) => {
      state.form.module_id = null
      state.moduleList = []
      state.moduleQuery.project_id = project_id

      getModuleList()
    }
    //  ----------------module start-------------------------------------
    // 获取模块列表
    const getModuleList = () => {
      useModuleApi().getList(state.moduleQuery)
          .then(res => {
            state.moduleList = res.data.rows
          })
    }

    onMounted(() => {
      getProjectList()
    })
    return {
      formRef,
      setData,
      getData,
      getProjectList,
      getModuleList,
      selectProject,
      ...toRefs(state),
    };
  },
});
</script>


<style lang="scss" scoped>
:deep(.el-transfer-panel .el-transfer-panel__header) {
  height: 30px !important;
}

:deep(.el-transfer-panel__filter .el-input__inner) {
  height: 26px !important;
}

:deep(.el-transfer-panel .el-transfer-panel__header .el-checkbox .el-checkbox__label) {
  font-size: 12px;
  font-weight: bold;
}

:deep(.el-input__inner) {
  font-weight: bold;
}
</style>