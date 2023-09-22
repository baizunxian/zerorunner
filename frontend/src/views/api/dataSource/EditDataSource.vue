<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable :title="state.editType === 'save'? '新增' : '修改'" v-model="state.isShowDialog" width="40%">
      <el-form :model="state.form" :rules="state.rules" ref="formRef" label-width="auto">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="数据源名称" prop="name">
              <el-input v-model="state.form.name" placeholder="请输入数据源名称" clearable></el-input>
            </el-form-item>
          </el-col>

          <!--          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">-->
          <!--            <el-form-item label="关联环境" prop="type">-->
          <!--              <el-select v-model="form.env_id" clearable placeholder="选择关联环境" style="width: 100%">-->
          <!--                <el-option-->
          <!--                    v-for="env in envList"-->
          <!--                    :key="env.id"-->
          <!--                    :label="env.name"-->
          <!--                    :value="env.id"-->
          <!--                >-->
          <!--                </el-option>-->
          <!--              </el-select>-->
          <!--            </el-form-item>-->
          <!--          </el-col>-->

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="数据源类型" prop="type">
              <el-select v-model="state.form.type" clearable placeholder="选择数据源类型" style="width: 100%">
                <el-option
                    v-for="item in state.dataSourceType"
                    :key="item"
                    :label="item"
                    :value="item"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="地址" prop="host">
              <el-input v-model="state.form.host" placeholder="请输入地址" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="端口" prop="port">
              <el-input v-model.number="state.form.port" placeholder="请输入端口" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="用户名" prop="user">
              <el-input v-model="state.form.user" placeholder="请输入用户名" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="state.form.password" placeholder="请输入密码" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onDialog">取 消</el-button>
					<el-button type="primary" @click="testConnect">测试连接</el-button>
					<el-button type="primary" @click="saveOrUpdate" :disabled="!state.isTestConnect">保 存</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="EditDataSource">
import {reactive, ref, watch} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {ElMessage} from "element-plus";
import {useEnvApi} from "/@/api/useAutoApi/env";

const emit = defineEmits(['getList'])

const createForm = () => {
  return {
    id: null,
    name: "",
    type: "mysql",
    host: "",
    port: "",
    user: "",
    password: "",
  }
}
const formRef = ref()
const state = reactive({
  dataSourceType: ['mysql'],
  isShowDialog: false,
  isTestConnect: false,
  editType: '',
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入数据源名称', trigger: 'blur'},],
    host: [{required: true, message: '请选数据源地址', trigger: 'blur'},],
    env_id: [{required: true, message: '请选数环境', trigger: 'blur'},],
    port: [{required: true, message: '请输入端口号', trigger: 'blur'},],
    user: [{required: true, message: '请输入用户名', trigger: 'blur'},],
    password: [{required: true, message: '请输入密码', trigger: 'blur'},],
  },

  // environment
  envList: [],
  envListQuery: {
    page: 1,
    pageSize: 200,
  }
});

// 打开弹窗
const openDialog = (type, row) => {
  // 获取项目列表
  state.editType = type
  state.isTestConnect = false
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
  } else {
    state.form = createForm()
  }
  onDialog();
  // getEnvList()
};
// 关闭弹窗
const onDialog = () => {
  state.isShowDialog = !state.isShowDialog;
};
// 测试数据源连接
const testConnect = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      useQueryDBApi().testConnect(state.form).then((res) => {
        let {data} = res
        if (data) {
          state.isTestConnect = true
          ElMessage.success("测试连接成功")
        } else {
          ElMessage.warning("测试连接失败！")
        }
      })
    }
  })
}
// 新增
const saveOrUpdate = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      useQueryDBApi().saveOrUpdate(state.form)
        .then(() => {
          ElMessage.success('操作成功');
          emit('getList')
          onDialog(); // 关闭弹窗
        })
    }
  })
};

// environment
const getEnvList = () => {
  useEnvApi().getList(state.envListQuery)
    .then(res => {
      state.envList = res.data.rows
    })
};

watch(
  () => state.form,
  () => {
    state.isTestConnect = false
  },
  {deep: true}
)

defineExpose({
  openDialog,
})
</script>
