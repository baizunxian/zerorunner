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

      <messages ref="messagesRef"/>

      <!--        <h3 class="block-title">参数信息</h3>-->
      <div style="min-height: 500px">
        <el-tabs v-model="activeName">
          <!--            <el-tab-pane name='requestBody'>-->
          <!--              <template #label><strong>body</strong></template>-->
          <!--              <request-body ref="requestBodyRef"/>-->
          <!--            </el-tab-pane>-->

          <el-tab-pane name='httpConfig'>
            <template #label><span>HTTP配置</span></template>
            <http-config ref="httpConfigRef"/>
          </el-tab-pane>

          <!--            <el-tab-pane name='extractValidate'>-->
          <!--              <template #label><strong>提取/校验</strong></template>-->
          <!--              <extract-validate ref="extractValidateRef"/>-->
          <!--            </el-tab-pane>-->

          <el-tab-pane name='commonConfig'>
            <template #label><span>通用配置</span></template>
            <common-config ref="commonConfigRef"/>
          </el-tab-pane>

          <el-tab-pane name='databaseConfig'>
            <template #label><span>数据库配置</span></template>
            <database-config ref="databaseConfigRef"/>
          </el-tab-pane>

        </el-tabs>
      </div>
    </div>
    <!--    </el-card>-->

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue'
import Messages from '/@/views/api/environment/components/messages.vue'
import httpConfig from '/@/views/api/environment/components/httpConfig.vue'
import commonConfig from '/@/views/api/environment/components/commonConfig.vue'
import databaseConfig from '/@/views/api/environment/components/databaseConfig.vue'
import {ElMessage} from "element-plus"
import {useStore} from "/@/store"
import {useRoute, useRouter} from "vue-router"
import {useEnvApi} from '/@/api/useAutoApi/env'
import type {PropType} from 'vue'

export default defineComponent({
  name: 'saveOrUpdateEnv',
  components: {
    Messages,
    httpConfig,
    commonConfig,
    databaseConfig,
  },
  props: {
    env_id: {
      type: [Number, null] as PropType<Number | null>,
      default: () => null,
    },
  },
  setup(props) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const messagesRef = ref()
    const httpConfigRef = ref()
    const databaseConfigRef = ref()
    const commonConfigRef = ref()
    const state = reactive({
      isShowDialog: false,
      activeName: 'httpConfig',

    });


    const saveOrUpdate = () => {
      try {
        // 获取url mothod 表单
        let msgData = messagesRef.value.getData()
        let httpData = httpConfigRef.value.getData()
        let commonData = commonConfigRef.value.getData()
        // let databaseData = databaseConfigRef.value.getData()

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
          let case_id = res.data
          messagesRef.value.setId(case_id)
        })
      } catch (err: any) {
        ElMessage.info(err || '信息表单填写不完整')
      }
    }

    const setData = async () => {
      let data = null
      if (props.env_id) {
        let res = await useEnvApi().getEnvById({id: props.env_id})
        data = res.data
      }
      messagesRef.value.setData(data)
      httpConfigRef.value.setData(data)
      commonConfigRef.value.setData(data)
      databaseConfigRef.value.setData(data)
    }

    // 返回到列表
    const goBack = () => {
      router.push({name: 'apiTestCase'})
    }

    onMounted(() => {
      setData()
    })

    return {
      messagesRef,
      httpConfigRef,
      databaseConfigRef,
      commonConfigRef,
      store,
      route,
      router,
      goBack,
      saveOrUpdate,
      ...toRefs(state),
    };
  },
});
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