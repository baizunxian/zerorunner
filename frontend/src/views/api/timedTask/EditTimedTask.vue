<template>
  <div class="system-edit-menu-container">
    <el-dialog
        class="task-content"
        draggable
        top="5vh"
        :title="state.editType === 'save'? '新增' : '修改'"
        v-model="state.isShowDialog" width="70%">
      <el-row>
        <el-col :span="10" class="task-card">
          <el-card>
            <el-form :model="state.form" :rules="state.rules" ref="formRef" label-width="80px">
              <el-row :gutter="35">

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="所属项目" prop="project_id">
                    <el-select
                        v-model="state.form.project_id"
                        placeholder="选择项目"
                        filterable style="width: 100%;">
                      <el-option
                          v-for="project in state.projectList"
                          :key="project.id + project.name"
                          :label="project.name"
                          :value="project.id">
                        <span style="float: left">{{ project.name }}</span>
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">

                  <el-form-item label="任务标签" prop="tags">
                    <el-tag
                        v-for="tag in state.form.task_tags"
                        :key="tag"
                        size="default"
                        type="success"
                        closable
                        style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                        :disable-transitions="false"
                        @close="removeTag(tag)">
                      {{ tag }}
                    </el-tag>

                    <el-input
                        v-if="state.editTag"
                        ref="caseTagInputRef"
                        v-model="state.tagValue"
                        class="ml-1 w-20"
                        size="small"
                        @keyup.enter="addTag"
                        @blur="addTag"
                        style="width: 100px"
                    />
                    <el-button v-else size="small" @click="showEditTag">
                      + New Tag
                    </el-button>
                  </el-form-item>

                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="任务名称" prop="name">
                    <el-input size="small" v-model="state.form.name" placeholder="请输入任务名" clearable></el-input>
                  </el-form-item>
                </el-col>


                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="任务描述" prop="description">
                    <el-input v-model="state.form.description"
                              placeholder="任务描述">
                    </el-input>
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="任务线程数" prop="threads_number">
                    <el-input-number v-model="state.form.threads_number" :max="30"
                                     placeholder="线程数">
                    </el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-tabs v-model="state.form.task_type" @tab-change="changeScheduleMode">
                    <el-tab-pane label="Crontab" name="crontab">
                      <el-form-item label="crontab" prop="crontab" style="width: 100%">
                        <div style="display: flex; width: 100%">
                          <el-input v-model="state.form.crontab"
                                    auto-complete="off"
                                    style="width: 80%; padding-right: 5px"
                                    placeholder="crontab表达式 例如： 11 * * * *">
                          </el-input>
                        </div>
                      </el-form-item>
                    </el-tab-pane>

                    <el-tab-pane label="Interval" name="interval">
                      <el-tabs v-model="state.form.interval_period">
                        <el-tab-pane v-for="item in state.intervalPeriod"
                                     :label="item"
                                     :name="item"
                                     :key="item">
                          <el-input-number v-model="state.form.interval_every"
                                           :min="1"
                                           controls-position="right">
                          </el-input-number>
                        </el-tab-pane>
                      </el-tabs>
                    </el-tab-pane>

                  </el-tabs>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </el-col>
        <el-col :span="14" class="task-card">
          <el-card>
            <el-tabs v-model="state.activeTabName">
              <el-tab-pane label="用例" name="case">
                <CaseInfo :task_id="state.form.id"
                          :envId="state.form.case_env_id"
                          ref="taskCaseInfoRef"></CaseInfo>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>

      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onDialog">取 消</el-button>
					<el-button type="primary" @click="saveOrUpdate">保 存</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="saveOrUpdateTimedTasks">
import {nextTick, onMounted, reactive, ref} from 'vue';
import {useTimedTasksApi} from "/@/api/useAutoApi/timedTasks";
import {ElButton, ElMessage} from "element-plus";
import {useProjectApi} from "/@/api/useAutoApi/project";
import CaseInfo from "./caseInfo.vue"

const emit = defineEmits(["getList"])

const createForm = () => {
  return {
    id: null,
    name: '', // 项目名称
    project_id: null, // project
    responsible_name: '', // 负责人
    run_type: 'module', // 默认模块类型
    case_ids: [], // id集合
    crontab: '', // 表达式
    task_type: "crontab",
    description: '', // 备注
    task_tags: [], // tags
    threads_number: 10, // 线程数
    case_env_id: null, // 用例环境id
    interval_period: "",
    interval_every: 1,
  }
}
const formRef = ref()
const caseTagInputRef = ref()
const taskCaseInfoRef = ref()
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
  },
  // tags
  editTag: false,
  tagValue: "",
  // tabs
  activeTabName: 'case',

  // crontab
  isCheckCrontab: false,
  crontabRunDate: [],

  //interval
  intervalActiveDateName: "hours",
  intervalPeriod: ["days", "hours", "minutes", "seconds"]
});
// 获取项目列表
const getProjectList = () => {
  useProjectApi().getList(state.projectListQuery)
      .then(res => {
        state.projectList = res.data.rows
      })
};


// 切换运行类型时清空
const radioChange = () => {
  state.form.case_ids = []
}

// 打开弹窗
const openDialog = (type, row) => {
  // 获取项目列表
  state.editType = type
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
  } else {
    state.form = createForm()
  }

  nextTick(() => {
    taskCaseInfoRef.value.initData(state.form.id, state.form.case_env_id)
  })

  onDialog();
};
// 关闭弹窗
const onDialog = () => {
  state.isShowDialog = !state.isShowDialog;
};
// 新增
const saveOrUpdate = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      let caseEnvId = taskCaseInfoRef.value.getCaseEnvId()
      let caseIds = taskCaseInfoRef.value.getCaseIds()
      if (caseIds.length === 0) {
        return ElMessage.warning("请选择需要执行的用例!")
      }
      if (!caseEnvId) {
        return ElMessage.warning("请选择api运行环境!")
      }
      state.form.case_ids = caseIds
      state.form.case_env_id = caseEnvId

      useTimedTasksApi().saveOrUpdate(state.form)
          .then(() => {
            ElMessage.success('操作成功');
            emit('getList')
            onDialog(); // 关闭弹窗
          })
    }
  })
};


// tags
const showEditTag = () => {
  state.editTag = true
  nextTick(() => {
    caseTagInputRef.value?.input.focus()
  })
}

const addTag = () => {
  if (state.editTag && state.tagValue) {
    if (!state.form.task_tags) state.form.task_tags = []
    state.form.task_tags.push(state.tagValue)
  }
  state.editTag = false
  state.tagValue = ''
}
const removeTag = (tag) => {
  state.form.task_tags.splice(state.form.task_tags.indexOf(tag), 1)
}

// checkCrontab
const checkCrontab = () => {
  useTimedTasksApi().checkCrontab({crontab: state.form.crontab}).then((res) => {
    state.isCheckCrontab = true
    state.crontabRunDate = res.data
  })
}

// changeScheduleMode
const changeScheduleMode = (val) => {
  if (val === 'interval' && !state.form.interval_period) {
    state.form.interval_period = "hours"
    state.form.interval_every = 1
  }
}

// 页面加载时
onMounted(() => {
  getProjectList();
});

defineExpose({
  openDialog,
})

</script>

<style lang="scss" scoped>
.task-card {
  padding: 0 8px;

  :deep(.el-card__body) {
    height: 65vh;
  }
}

//:deep(.task-content .el-dialog__body) {
//  height: 68vh;
//}

</style>