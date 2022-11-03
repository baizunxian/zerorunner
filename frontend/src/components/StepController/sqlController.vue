<template>

  <el-collapse-transition>
    <div v-show="data.showDetail" @click.stop="">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <div style="border: 1px solid #E6E6E6; padding: 8px">

        <el-form ref="formRef"
                 :model="data"
                 label-width="auto"
                 label-position="left"
        >

          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb10">
              <el-form-item label="运行环境" prop="project_id">
                <el-select size="small" v-model="data.env_id" placeholder="运行环境" filterable
                           style="width: 100%;"
                           @change="selectEnv(data.env_id)">
                  <el-option
                      v-for="env in envList"
                      :key="env.id + env.name"
                      :label="env.name"
                      :value="env.id">
                    <span style="float: left">{{ env.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb10">
              <el-form-item label="数据源名称" prop="module_id">
                <el-select size="small" v-model="data.source_id" placeholder="请选择" filterable
                           style="width: 100%;">
                  <el-option
                      v-for="source in sourceList"
                      :key="source.id + source.name"
                      :label="source.name"
                      :value="source.id">
                    <span style="float: left">{{ source.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb10">
              <el-form-item label="超时时间" prop="config_id">
                <el-input-number size="small" v-model="data.timeout" placeholder="秒"/>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" class="mb10">
              <el-form-item label="存储结果" prop="variable_name" >
                <el-input size="small" v-model="data.variable_name" placeholder="查询结果赋值的变量名称"/>
              </el-form-item>
            </el-col>
          </el-row>

          <span class="el-form-item__label">SQL</span>
          <div style="border: 1px solid #E6E6E6">
            <monaco-editor
                style="height: 150px"
                ref="monacoEditRef"
                v-model:value="data.value"
            ></monaco-editor>
          </div>

        </el-form>

      </div>
    </div>
  </el-collapse-transition>

</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs} from 'vue';
import {useEnvApi} from "/@/api/useAutoApi/env";
import {useQueryDBApi} from "/@/api/useTools/querDB";


export default defineComponent({
  name: 'sqlController',
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup() {
    const state = reactive({
      // sourceList
      sourceList: [],
      dataSourceQuery: {
        page: 1,
        pageSize: 200,
        env_id: null,
      },
      // env
      envList: [],
      envQuery: {
        page: 1,
        pageSize: 200
      }

    });

    // selectEnv

    const selectEnv = (env_id: number) => {
      state.dataSourceQuery.env_id = env_id
      getDataSourceList()
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
      useQueryDBApi().getSourceList(state.dataSourceQuery)
          .then(res => {
            state.sourceList = res.data.rows
          })
    };

    onMounted(() => {
      getEnvList()
    })

    return {
      selectEnv,
      getEnvList,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

</style>