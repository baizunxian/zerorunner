<template>
  <el-dialog
      draggable
      title="修改密码"
      v-model="state.isShowDialog"
      width="40%">
    <el-form ref="formRef" :model="state.form" :rules="state.rules" label-width="80px">
      <el-row :gutter="35">
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
          <el-form-item label="旧密码"
                        prop="old_pwd"
                        :rules="[{ required: true, message: '请输入旧密码', trigger: 'blur' }]">
            <el-input type="password" v-model="state.form.old_pwd" placeholder="旧密码" clearable></el-input>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
          <el-form-item label="新密码"
                        prop="new_pwd"
                        :rules="[{ required: true, message: '请输入新密码', trigger: 'blur' }]">
            <el-input type="password" v-model="state.form.new_pwd" placeholder="新密码" clearable></el-input>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
          <el-form-item label="确认密码"
                        prop="re_new_pwd"
                        :rules="[{ required: true, trigger: 'blur', validator: validateReNewPwd }]">
            <el-input type="password" v-model="state.form.re_new_pwd" placeholder="确认密码" clearable></el-input>
          </el-form-item>
        </el-col>

      </el-row>
    </el-form>
    <template #footer>
				<span class="dialog-footer">
					<el-button @click="state.isShowDialog = !state.isShowDialog">取 消</el-button>
					<el-button type="primary" @click="resetPassword">提交</el-button>
				</span>
    </template>
  </el-dialog>

</template>

<script setup>
import {reactive, ref} from 'vue';
import {useUserApi} from "/@/api/useSystemApi/user";
import {ElMessage} from "element-plus";

const formRef = ref()
const state = reactive({
  form: {
    old_pwd: '',
    new_pwd: '',
    re_new_pwd: ''
  },
  isShowDialog: false
})

const validateReNewPwd = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入确认密码'))
  } else if (value !== state.form.new_pwd) {
    callback(new Error("两次输入密码不一致"))
  } else {
    callback()
  }
}

const resetPassword = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      useUserApi().resetPassword(state.form).then(() => {
        state.isShowDialog = false
        ElMessage.success('修改成功， 下次登录请使用新密码登录😊')
      })
    }
  })
}

const openDialog = (userInfos) => {
  state.form = {}
  state.form.id = userInfos.id
  state.isShowDialog = !state.isShowDialog
}

defineExpose({
  openDialog
})

</script>

<style scoped lang="scss">

</style>