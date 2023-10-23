<template>

  <el-collapse-transition>
    <div v-show="step.showDetail" @click.stop="">
      <div style="border: 1px solid #E6E6E6; padding: 8px">
        <el-form ref="formRef"
                 :model="step">
          <el-row :gutter="24">
            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="运行环境" prop="project_id">
                <el-select size="small"
                           v-model="step.request.env_id"
                           placeholder="运行环境"
                           filterable
                           style="width: 100%;"
                           @change="selectEnv">
                  <el-option
                      v-for="env in state.envList"
                      :key="env.id + env.name"
                      :label="env.name"
                      :value="env.id">
                    <span style="float: left">{{ env.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="数据源名称" prop="module_id">
                <el-select size="small" v-model="step.request.source_id" placeholder="请选择" filterable
                           style="width: 100%;">
                  <el-option
                      v-for="source in state.sourceList"
                      :key="source.id + source.name"
                      :label="source.name"
                      :value="source.data_source_id">
                    <span style="float: left">{{ source.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="超时时间" prop="config_id">
                <el-input-number size="small" v-model="step.request.timeout" placeholder="秒"/>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="存储结果" prop="variable_name">
                <el-input size="small"
                          style="width: 100%"
                          v-model="step.request.variable_name"
                          placeholder="查询结果赋值的变量名称">
                  <template #suffix>
                    <span v-show="step.request.variable_name.length > 0" class="el-input__suffix-inner"
                          @click="copyText('${'+ step.request.variable_name +'}')">
                    <el-icon color="#303133">
                      <ele-DocumentCopy/>
                    </el-icon>
                  </span>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <span class="el-form-item__label">SQL</span>
          <div style="border: 1px solid #E6E6E6">
            <z-monaco-editor
                style="height: 150px"
                ref="monacoEditRef"
                lang="sql"
                v-model:value="step.request.sql"
                :options="{minimap: {enabled: false}}"
            />
          </div>

        </el-form>

      </div>
    </div>
  </el-collapse-transition>

</template>

<script setup name="SqlController">
import {nextTick, onMounted, reactive} from 'vue';
import {useEnvApi} from "/@/api/useAutoApi/env";
import commonFunction from '/@/utils/commonFunction';
import useVModel from "/@/utils/useVModel";

const {copyText} = commonFunction()

const props = defineProps({
  step: {
    type: Object,
    required: true
  }

})

const emit = defineEmits(['update:step'])

const step = useVModel(props, 'step', emit)
const state = reactive({
  // sourceList
  sourceList: [],
  dataSourceQuery: {
    page: 1,
    pageSize: 1000,
    env_id: 0,
  },
  // environment
  envList: [],
  envQuery: {
    page: 1,
    pageSize: 200
  },

});

// selectEnv
const selectEnv = (env_id) => {
  if (env_id) {
    state.dataSourceQuery.env_id = env_id
    getDataSourceList()
  }
  step.value.request.source_id = null
}

// 初始化env
const getEnvList = () => {
  useEnvApi().getList(state.envQuery)
      .then(res => {
        state.envList = res.data.rows
      })
};

// 初始化datasource
const getDataSourceList = () => {
  useEnvApi().getDataSourceByEnvId(state.dataSourceQuery)
      .then(res => {
        state.sourceList = res.data
      })
};

onMounted(() => {
  getEnvList()
  nextTick(() => {
    if (props.step.request?.env_id) {
      state.dataSourceQuery.env_id = step.value.request.env_id
      getDataSourceList()
    }
  })
})


</script>

<style>
.no-touch {
  touch-action: none;
}
</style>