<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        :title="editType === 'save'? '新增' : '修改'"
        v-model="isShowDialog" width="40%">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="任务名称" prop="name">
              <el-input size="small" v-model="form.name" placeholder="请输入任务名" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="所属项目" prop="project_id">
              <el-select
                  v-model="form.project_id"
                  placeholder="选择项目"
                  filterable style="width: 100%;"
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

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="执行时间" prop="crontab_str">
              <el-input v-model="form.crontab_str" auto-complete="off" placeholder="crontab表达式 例如： 11 * * * *">
              </el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="套件类型" prop="run_type">
              <el-radio-group v-model="form.run_type" size="small" @change="radioChange">
                <!-- <el-radio :label="1" border>项目</el-radio> -->
                <el-radio label="module" border>模块</el-radio>
                <el-radio label="suite" border>套件</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>


          <!--          项目-->
          <template v-if="form.run_type === 'module'">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="关联模块" prop="case_ids">
                <el-select
                    multiple
                    collapse-tags
                    v-model="form.case_ids"
                    placeholder="选择模块"
                    filterable style="width: 100%;">
                  <el-option
                      v-for="module in moduleList"
                      :key="module.id + module.name"
                      :label="module.name"
                      :value="module.id">
                    <span style="float: left">{{ module.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </template>

          <!--          套件-->
          <template v-if="form.run_type === 'suite'">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="关联套件" prop="module_ids">
                <el-select
                    multiple
                    collapse-tags
                    v-model="form.case_ids"
                    placeholder="选择套件"
                    filterable style="width: 100%;"
                >
                  <el-option
                      v-for="suite in suiteList"
                      :key="suite.id + suite.name"
                      :label="suite.name"
                      :value="suite.id">
                    <span style="float: left">{{ suite.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </template>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="备注" prop="description">
              <el-input v-model="form.description" type="textarea" auto-complete="off" placeholder="备注">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onDialog">取 消</el-button>
					<el-button type="primary" @click="saveOrUpdate">保 存</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue';
import {useTimedTasksApi} from "/@/api/useAutoApi/timedTasks";
import {ElMessage} from "element-plus";
import {useProjectApi} from "/@/api/useAutoApi/project";
import {useModuleApi} from "/@/api/useAutoApi/module";
import {useTestSuiteApi} from "/@/api/useAutoApi/suite";

export default defineComponent({
  name: 'saveOrUpdateTimedTasks',
  setup(props, {emit}) {
    const createForm = () => {
      return {
        id: null,
        name: '', // 项目名称
        project_id: null, // project
        responsible_name: '', // 负责人
        run_type: 'module', // 默认模块类型
        case_ids: [], // id集合
        crontab_str: '', // 表达式
        description: '', // 备注
      }
    }
    const formRef = ref()
    const state = reactive({
      isShowDialog: false,
      editType: '',
      // showCronBox
      showCronBox: false,

      form: createForm(),
      rules: {
        name: [{required: true, message: '请输入模块名称', trigger: 'blur'},],
        project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'},],
        crontab_str: [{required: true, message: '请输入执行时间', trigger: 'blur'},],
        case_ids: [{required: true, message: '请选择关联配置', trigger: 'blur'},],
      },
      // project
      projectList: [], // 项目数据
      projectListQuery: {   //
        page: 1,
        pageSize: 1000,
        name: '',
      },
      // module
      moduleList: [], // 模块数据
      moduleListQuery: {   //
        page: 1,
        pageSize: 1000,
        project_id: null,
        name: '',
      },
      // suite
      suiteList: [], // 套件数据
      suiteListQuery: {   //
        page: 1,
        pageSize: 1000,
        project_id: null,
        name: '',
      }
    });
    // 获取项目列表
    const getProjectList = () => {
      useProjectApi().getList(state.projectListQuery)
          .then(res => {
            state.projectList = res.data.rows
          })
    };

    // 获取套件
    const getSuitesList = () => {
      useTestSuiteApi().getList(state.suiteListQuery)
          .then(res => {
            state.suiteList = res.data.rows
          })
    };

    // 选择项目
    const selectProject = (project_id: any) => {
      state.form.case_ids = []
      if (state.form.run_type === 'module') {
        state.moduleListQuery.project_id = project_id
        getModuleList()
      } else if (state.form.run_type === 'suite') {
        state.suiteListQuery.project_id = project_id
        getSuitesList()
      }

    }

    // 模块 module
    const getModuleList = () => {
      useModuleApi().getList(state.moduleListQuery)
          .then(res => {
            state.moduleList = res.data.rows
          })
    };
    // 获取套件列表
    // const getProjectList = () => {
    //   useProjectApi().getList(state.projectListQuery)
    //       .then(res => {
    //         state.projectList = res.data.rows
    //       })
    // };

    // 切换运行类型时清空
    const radioChange = () => {
      state.form.case_ids = []
    }

    // 打开弹窗
    const openDialog = (type: string, row: any) => {
      // 获取项目列表
      state.editType = type
      if (row) {
        state.form = JSON.parse(JSON.stringify(row));
        if (row.run_type === 'module') {
          state.moduleListQuery.project_id = row.project_id
          getModuleList()
        }
        else if (row.run_type === 'suite') {
          state.suiteListQuery.project_id = row.project_id
          getSuitesList()
        }
      } else {
        state.form = createForm()
      }
      onDialog();
    };
    // 关闭弹窗
    const onDialog = () => {
      state.isShowDialog = !state.isShowDialog;
    };
    // 新增
    const saveOrUpdate = () => {
      formRef.value.validate((valid: any) => {
        if (valid) {
          useTimedTasksApi().saveOrUpdate(state.form)
              .then(() => {
                ElMessage.success('操作成功');
                emit('getList')
                onDialog(); // 关闭弹窗
              })
        }
      })
      console.log(state.form, 'state.menuForm')
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };
    // 页面加载时
    onMounted(() => {
      getProjectList();
    });

    return {
      selectProject,
      getProjectList,
      getModuleList,
      getSuitesList,
      openDialog,
      radioChange,
      formRef,
      onDialog,
      saveOrUpdate,
      ...toRefs(state),
    };
  },
});
</script>
