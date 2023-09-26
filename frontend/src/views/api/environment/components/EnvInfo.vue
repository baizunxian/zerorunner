<template>
  <el-form ref="formRef"
           :model="state.data"
           label-width="80px"
           label-position="left"
           :rules="state.rules">
    <el-row :gutter="24">
      <el-col :span="10">
        <el-form-item label="环境名称" prop="name">
          <el-input v-model.trim="state.data.name" style="width: 100%;" placeholder="请输入环境名称"></el-input>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup name="EnvInfo">
import {onMounted, reactive, ref} from "vue";

const formRef = ref()
const createData = () => {
  return {
    id: null,
    name: '',
  }
}
const state = reactive({
  isShowDialog: false,
  handleType: '',   //apiInfo 调用类型， 保存，调试
  // 表单及校验
  data: createData(),
  rules: {
    name: [{required: true, message: '请输入环境名称', trigger: 'blur'}],
  },


});
// 获取表单数据
const getData = () => {
  return state.data
}

// 初始化表单
const setData = (data) => {
  state.data = createData()
  if (data) state.data = data
}

// 回填id
const setId = (id) => {
  state.data.id = id
}


onMounted(() => {
})

defineExpose({
  setData,
  getData,
  setId,
})

</script>


<style lang="scss" scoped>

</style>