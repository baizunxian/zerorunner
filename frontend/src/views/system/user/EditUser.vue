<template>
  <div class="system-edit-user-container">
    <el-dialog
        draggable
        :title="state.editType === 'save'? `新增` : `修改`"
        v-model="state.isShowDialog" width="769px">
      <el-form :model="state.form" :rules="state.rules" ref="userFormRef" size="default" label-width="90px">
        <el-row :gutter="35">

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="账户名称" prop="username">
              <el-input :disabled="state.editType==='update'" v-model="state.form.username" placeholder="请输入账户名称"
                        clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="用户昵称" prop="nickname">
              <el-input v-model="state.form.nickname" placeholder="请输入用户昵称" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="关联角色" prop="roles">
              <el-select v-model="state.form.roles" multiple placeholder="请选择" clearable class="w100">
                <el-option
                    v-for="item in roleList"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="state.form.email" placeholder="请输入" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="用户状态">
              <el-switch v-model="state.form.status"
                         :active-value="1"
                         :inactive-value="0"
                         inline-prompt
                         active-text="启"
                         inactive-text="禁"></el-switch>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="用户类型">
              <el-select v-model="state.form.user_type" placeholder="请选择" clearable class="w100">
                <el-option label="超级管理员" :value="10"></el-option>
                <el-option label="普通用户" :value="20"></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="用户备注">
              <el-input v-model="state.form.remarks" type="textarea" placeholder="请输入用户描述"
                        maxlength="150"></el-input>
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

<script lang="ts" setup name="SaveOrUpdateUser">
import {reactive, ref} from 'vue';
import {useUserApi} from "/@/api/useSystemApi/user";
import {ElMessage} from "element-plus";

const emit = defineEmits(["getList"])

const props = defineProps({
  roleList: {
    type: Array,
    default: () => []
  }
})

const createForm = () => {
  return {
    id: null, // 账户名称
    username: '', // 账户名称
    nickname: '', // 用户昵称
    roles: '', // 关联角色
    email: '', // 邮箱
    status: 1, // 用户状态 1启用 2 禁用
    user_type: 20, // 用户类型
    remarks: '', // 描述
    updated_by: null, // 更新人
  }
}

const userFormRef = ref()
const state = reactive({
  isShowDialog: false,
  editType: 'save',
  form: createForm(),
  rules: {
    username: [{required: true, message: '请输入用户名称', trigger: 'blur'},],
    roles: [{required: true, message: '请选择角色', trigger: 'blur'},],
    nickname: [{required: true, message: '请输入用户昵称', trigger: 'blur'},],
  }
});

// 新增修改窗口初始化
const openDialog = (editType: string, row: any) => {
  state.editType = editType
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
// 更新-新增
const saveOrUpdate = () => {
  userFormRef.value.validate((valid: any) => {
    if (valid) {
      useUserApi().saveOrUpdate(state.form)
          .then(() => {
            ElMessage.success('操作成功');
            emit('getList')
            closeDialog(); // 关闭弹窗
          })
    }
  })

};

defineExpose({
  openDialog,

})

</script>
