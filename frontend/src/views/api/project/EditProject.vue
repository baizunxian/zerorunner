<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        :title="state.editType === 'save'? '新增' : '修改'" v-model="state.isShowDialog"
        width="30%">
      <el-form ref="formRef" :model="state.form" :rules="state.rules" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="state.form.name" placeholder="项目名称" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="负责人">
              <el-input v-model="state.form.responsible_name" placeholder="负责人" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="测试人员">
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
					<el-button @click="onCancel">取 消</el-button>
					<el-button type="primary" @click="saveOrUpdate">保 存</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="saveOrUpdateProject">
import {reactive, ref} from 'vue';
import {useProjectApi} from "/@/api/useAutoApi/project";
import {ElMessage} from "element-plus";

const emit = defineEmits(["getList"])

const createForm = () => {
  return {
    name: '', // 项目名称
    project_id: '', // 项目id
    config_id: null, // 配置id
    leader_user: '', // 负责人
    test_user: '', // 测试负责人
    publish_app: '', // 关联应用
    simple_desc: '', // 简要描述
    remarks: '', // 简要描述
    priority: '', // 优先级
    module_packages: null, // 配置信息
  }
}
const formRef = ref()
const state = reactive({
  isShowDialog: false,
  editType: '',
  // 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入项目名称', trigger: 'blur'},],
  },
  menuData: [], // 上级菜单数据
});


// 打开弹窗
const openDialog = (type, row) => {
  state.editType = type
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
  } else {
    state.form = createForm()
  }
  state.isShowDialog = true;
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};
// 新增
const saveOrUpdate = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      useProjectApi().saveOrUpdate(state.form)
          .then(() => {
            ElMessage.success('操作成功');
            emit('getList')
            closeDialog(); // 关闭弹窗
          })
      console.log(state.form, 'state.menuForm')
    }
  })

};

defineExpose({
  openDialog,
})

</script>
