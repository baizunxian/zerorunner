<template>
  <div class="content">
    <div class="block-title">环境信息</div>
    <div style="padding: 10px 0">
      <el-form
          label-position="left"
          label-width="80px"
          :model="state.data"
          style="max-width: 500px"
      >
        <el-form-item label="环境域名">
          <el-input v-model="state.data.domain_name"/>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="state.data.remarks"/>
        </el-form-item>
      </el-form>
    </div>

    <div class="block-title">
      <div>请求头</div>

      <el-popover placement="right" :width="400" trigger="click" @show="showBulk">
<!--        <template #reference>-->
<!--          <el-button type="primary" link>批量添加</el-button>-->
<!--        </template>-->
        <el-input type="textarea" rows="20" show-word-limit v-model="state.headersBulk"></el-input>
        <el-button type="primary" link @click="addHeaders">添加</el-button>
      </el-popover>

    </div>

    <HeadersController ref="headersControllerRef" :data="state.data.headers"></HeadersController>

  </div>
</template>

<script setup name="httpConfig">
import {reactive, ref} from "vue";
import {handleEmpty} from "/@/utils/other";
import HeadersController from "/@/components/Z-StepController/headers/HeadersController.vue";

const headersControllerRef = ref()
const state = reactive({
  data: {
    name: "",  // 环境名称
    domain_name: "",  // 环境域名
    remarks: "",
    headers: [],  // 请求头数据

  },
  headersBulk: '',  // bulk内容

});
// 初始化数据
const setData = (data) => {
  if (data) {
    state.data.headers = data.headers ? data.headers : []
    state.data.remarks = data.remarks
    state.data.domain_name = data.domain_name
    state.data.name = data.name

  }
}

// 获取表单数据
const getData = () => {
  state.data.headers = handleEmpty(state.data.headers)
  return state.data
}

const showBulk = () => {
  state.headersBulk = headersControllerRef.value.keyValueToBulk()
}
const addHeaders = () => {
  headersControllerRef.value.bulkToKeyValue(state.headersBulk)
}

defineExpose({
  setData,
  getData,
})

</script>


<style lang="scss" scoped>
.block-title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 20px;
  line-height: 20px;
  background: #f7f7fc;
  color: #333333;
  border-left: 2px solid #409eff;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}
</style>