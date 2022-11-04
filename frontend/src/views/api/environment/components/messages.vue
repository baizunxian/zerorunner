<template>
  <el-form ref="formRef"
           :model="data"
           label-width="80px"
           label-position="left"
           :rules="rules">
    <el-row :gutter="24">
      <el-col :span="10">
        <el-form-item label="环境名称" prop="name">
          <el-input v-model.trim="data.name" style="width: 100%;" placeholder="请输入用例名称"></el-input>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from "vue";


export default defineComponent({
  name: 'case-url',
  components: {},
  setup() {
    const formRef = ref()
    const createData = () => {
      return {
        id: null,
        name: '',
      }
    }
    const state = reactive({
      isShowDialog: false,
      handleType: '',   //apiCase 调用类型， 保存，调试
      // 表单及校验
      data: createData(),
      rules: {
        name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
      },


    });
    // 获取表单数据
    const getData = () => {
      return state.data
    }

    // 初始化表单
    const setData = (data: any) => {
      state.data = createData()
      if (data) state.data = data
    }

    // 回填id
    const setId = (id: number | null) => {
      state.data.id = id
    }


    onMounted(() => {
    })
    return {
      formRef,
      setData,
      getData,
      setId,
      ...toRefs(state),
    };
  },
});
</script>


<style lang="scss" scoped>

</style>