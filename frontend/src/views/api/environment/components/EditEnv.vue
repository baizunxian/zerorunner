<template>
  <div class="system-edit-menu-container">
    <!--    <el-card class="save-update-card">-->
    <div>
      <!--        <el-page-header-->
      <!--            class="page-header"-->
      <!--            :content="editType === 'create'? '新增配置':'更新配置'"-->
      <!--            style="margin: 10px 0;"-->
      <!--            @back="goBack"-->
      <!--        >-->
      <!--        </el-page-header>-->

      <!--        <h3 class="block-title">请求信息</h3>-->

      <!--        <url ref="urlRef" @saveOrUpdateOrDebug="saveOrUpdateOrDebug"/>-->

      <!--        <h3 class="block-title">基本信息</h3>-->

      <EnvInfo ref="EnvInfoRef"/>

      <!--        <h3 class="block-title">参数信息</h3>-->
      <div style="min-height: 500px">
        <el-tabs v-model="state.activeName">
          <!--            <el-tab-pane name='requestBody'>-->
          <!--              <template #label><strong>body</strong></template>-->
          <!--              <request-body ref="requestBodyRef"/>-->
          <!--            </el-tab-pane>-->

          <el-tab-pane name='httpConfig'>
            <template #label><span>HTTP配置</span></template>
            <HttpConfig ref="httpConfigRef"/>
          </el-tab-pane>

          <!--            <el-tab-pane name='extractValidate'>-->
          <!--              <template #label><strong>提取/校验</strong></template>-->
          <!--              <extract-validate ref="extractValidateRef"/>-->
          <!--            </el-tab-pane>-->

          <el-tab-pane name='commonConfig'>
            <template #label><span>通用配置</span></template>
            <CommonConfig ref="commonConfigRef"/>
          </el-tab-pane>

          <el-tab-pane name='databaseConfig'>
            <template #label><span>数据库配置</span></template>
            <DatabaseConfig ref="databaseConfigRef"/>
          </el-tab-pane>

          <el-tab-pane name='funcConfig'>
            <template #label><span>辅助函数配置</span></template>
            <FuncConfig ref="funcConfigRef"/>
          </el-tab-pane>

        </el-tabs>
      </div>
    </div>

  </div>
</template>

<script setup name="EditEnv">
import {onMounted, reactive, ref} from 'vue'
import {ElMessage} from "element-plus"
import {useEnvApi} from '/@/api/useAutoApi/env'
import EnvInfo from '/@/views/api/environment/components/EnvInfo.vue'
import HttpConfig from '/@/views/api/environment/components/HttpConfig.vue'
import CommonConfig from '/@/views/api/environment/components/CommonConfig.vue'
import DatabaseConfig from '/@/views/api/environment/components/DatabaseConfig.vue'
import FuncConfig from '/@/views/api/environment/components/FuncConfig.vue'

const props = defineProps({
  env_id: {
    type: [Number, null],
    default: () => null,
  },
})


const EnvInfoRef = ref()
const httpConfigRef = ref()
const commonConfigRef = ref()
const databaseConfigRef = ref()
const funcConfigRef = ref()

const state = reactive({
  isShowDialog: false,
  activeName: 'httpConfig',

});


const saveOrUpdate = () => {
  try {
    // 获取url mothod 表单
    let msgData = EnvInfoRef.value.getData()
    let httpData = httpConfigRef.value.getData()
    let commonData = commonConfigRef.value.getData()

    // 组装表单
    let form = {
      id: msgData.id,
      name: msgData.name,
      headers: httpData.headers,
      domain_name: httpData.domain_name,
      remarks: httpData.remarks,
      variables: commonData.variables
    }
    // 保存用例
    useEnvApi().saveOrUpdate(form).then(res => {
      ElMessage.success('保存成功！')
      EnvInfoRef.value.setId(res.data.id)
    })
  } catch (err) {
    console.log(err)
    ElMessage.info(err || '信息表单填写不完整')
  }
}

const setData = async () => {
  let data = null
  if (props.env_id) {
    let res = await useEnvApi().getEnvById({id: props.env_id})
    data = res.data
  }
  EnvInfoRef.value.setData(data)
  httpConfigRef.value.setData(data)
  commonConfigRef.value.setData(data)
  databaseConfigRef.value.setData(data)
  funcConfigRef.value.setData(data)
}

defineExpose({
  saveOrUpdate
})

onMounted(() => {
  setData()
})

</script>

<style lang="scss" scoped>
:deep(.el-tabs__header) {
  margin: 0 0 6px;
}

.content {
  border: 1px solid #dcdfe6;
  border-radius: 5px;
  padding: 10px;
  margin: 5px 0;

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
  }
}

</style>