<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        :title="state.editType === 'save'? '新增' : '修改'" v-model="state.isShowDialog"
        width="30%">
      <el-form :model="state.form" :rules="state.rules" ref="formRef" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="模块名称" prop="name">
              <el-input v-model="state.form.name" placeholder="模块名称" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="所属项目" prop="project_id">
              <el-select v-model="state.form.project_id" clearable placeholder="选择所属项目" style="width: 100%">
                <el-option
                    v-for="item in state.projectList"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="负责人" prop="leader_user">
              <el-input v-model="state.form.leader_user" placeholder="负责人" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="测试人员" prop="test_user">
              <el-input v-model="state.form.test_user" placeholder="测试人员" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="开发人员">
              <el-input v-model="state.form.dev_user" placeholder="开发人员" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="关联应用">
              <el-input v-model="state.form.publish_app" placeholder="关联应用" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="简要描述">
              <el-input v-model="state.form.simple_desc" placeholder="简要描述" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="关联配置">
              <el-input v-model="state.form.config_id" placeholder="关联配置" clearable></el-input>
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

<script setup name="saveOrUpdateModule">
import {defineExpose, reactive, ref} from 'vue';
import {useProjectApi} from "/@/api/useAutoApi/project";
import {useModuleApi} from "/@/api/useAutoApi/module";
import {ElMessage} from "element-plus";

const emit = defineEmits(["getList"])

const createForm = () => {
  return {
    name: '', // 项目名称
    responsible_name: '', // 负责人
    test_user: '', // 测试人员
    dev_user: '', // 开发人员
    publish_app: '', // 关联应用
    simple_desc: '', // 简要描述
    config_id: null, // 配置信息
  }
}
const formRef = ref()
const state = reactive({
  isShowDialog: false,
  editType: '',
  // 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入模块名称', trigger: 'blur'},],
    project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'},],
  },
  projectList: [], // 项目数据
  projectListQuery: {   //
    page: 1,
    pageSize: 20,
    name: '',
  },
});

// 初始化表格数据
const getProjectList = () => {
  useProjectApi().getList(state.projectListQuery)
      .then(res => {
        state.projectList = res.data.rows
      })
};

// 打开弹窗
const openDialog = (type, row) => {
  // 获取项目列表
  getProjectList()
  state.editType = type
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
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
  formRef.value.validate((valid) => {
    if (valid) {
      useModuleApi().saveOrUpdate(state.form)
          .then(() => {
            ElMessage.success('操作成功');
            emit('getList')
            onDialog(); // 关闭弹窗
          })
    }
  })
};

defineExpose({
  openDialog,
})
</script>
