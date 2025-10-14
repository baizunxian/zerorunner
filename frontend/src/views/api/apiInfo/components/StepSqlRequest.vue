<template>
  <div @click.stop="">
    <div class="sql-request-box">
      <el-form ref="formRef" label-position="right" label-width="75px" :model="requestData">
        <el-row :gutter="24">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb10">
            <el-form-item label="连接配置" prop="project_id">
              <el-radio-group v-model="state.requestData.use_type">
                <el-radio-button label="source" value="source">数据源</el-radio-button>
                <el-radio-button label="custom" value="custom">自定义</el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <template v-if="state.requestData.use_type == 'source'">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb10">
              <el-form-item label="运行环境" prop="project_id">
                <el-select size="small" v-model="state.requestData.env_id" placeholder="运行环境" filterable
                           style="width: 100%" @change="selectEnv">
                  <el-option v-for="env in state.environments" :key="env.id + env.name" :label="env.name"
                             :value="env.id">
                    <span style="float: left">{{ env.name }}</span>
                  </el-option>

                  <template #prefix>
                    <el-icon
                        style="cursor: pointer; color: var(--el-color-primary)"
                        title="刷新环境"
                        @click.stop="
                												() => {
                													getEnvList();
                												}
                											"
                    >
                      <ele-Refresh/>
                    </el-icon>
                  </template>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb10">
              <el-form-item label="数据源名称" prop="module_id">
                <el-select size="small" v-model="state.requestData.source_id" placeholder="请选择" filterable
                           style="width: 100%">
                  <el-option v-for="source in state.sourceList" :key="source.id + source.name" :label="source.name"
                             :value="source.data_source_id">
                    <span style="float: left">{{ source.name }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </template>

          <template v-if="state.requestData.use_type == 'custom'">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb10">
              <el-form-item label="数据源类型" prop="source_type"
                            :rules="[{ required: true, message: '请选择数据源类型', trigger: 'blur' }]">
                <el-select v-model="state.requestData.source_type" clearable placeholder="选择数据源类型" style="width: 100%">
                  <el-option v-for="item in ['mysql']" :key="item" :label="item" :value="item"></el-option>
                </el-select>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="地址" prop="host"
                            :rules="[{ required: true, message: '请输入地址', trigger: 'blur' }]">
                <el-input v-model="state.requestData.host" placeholder="请输入地址" clearable></el-input>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="端口" prop="port"
                            :rules="[{ required: true, message: '请输入端口', trigger: 'blur' }]">
                <el-input v-model="state.requestData.port" placeholder="请输入端口" clearable></el-input>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="用户名" prop="user"
                            :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
                <el-input v-model="state.requestData.user" placeholder="请输入用户名" clearable></el-input>
              </el-form-item>
            </el-col>

            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
              <el-form-item label="密码" prop="password"
                            :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
                <el-input type="password" v-model="state.requestData.password" placeholder="请输入密码" clearable></el-input>
              </el-form-item>
            </el-col>
          </template>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">
            <el-form-item label="超时时间" prop="config_id">
              <el-input-number size="small" v-model="state.requestData.timeout" placeholder="秒"/>
            </el-form-item>
          </el-col>
        </el-row>

        <!--        <el-row>-->
        <!--          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb10">-->
        <!--            <el-form-item label="存储结果" prop="variable_name">-->
        <!--              <el-input size="small"-->
        <!--                        style="width: 100%"-->
        <!--                        v-model="stepData.request.variable_name"-->
        <!--                        placeholder="查询结果赋值的变量名称">-->
        <!--                <template #suffix>-->
        <!--                    <span v-show="stepData.request.variable_name.length > 0" class="el-input__suffix-inner"-->
        <!--                          @click="copyText('${'+ stepData.request.variable_name +'}')">-->
        <!--                    <el-icon color="#303133">-->
        <!--                      <ele-DocumentCopy/>-->
        <!--                    </el-icon>-->
        <!--                  </span>-->
        <!--                </template>-->
        <!--              </el-input>-->
        <!--            </el-form-item>-->
        <!--          </el-col>-->
        <!--        </el-row>-->

        <span class="el-form-item__label">SQL</span>
        <div class="sql-body">
          <z-monaco-editor
              style="min-height: 300px"
              ref="monacoEditRef"
              lang="sql"
              v-model:value="state.requestData.sql"
              :options="{ minimap: { enabled: false } }"
          />
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts" name="SqlController">
import { nextTick, onMounted, PropType, reactive, ref } from 'vue';
import { useEnvApi } from '/@/api/useAutoApi/env';
// import {useEnvironment} from '/@/stores/environment';
// import {storeToRefs} from 'pinia';
// import mittBus from '/@/utils/mitt';


// const storesEnvironment = useEnvironment();
// const {environments}: { environments: any } = storeToRefs(storesEnvironment);

const props = defineProps({
  requestData: {
    type: Object,
    required: true,
  },
  variableList: {
    type: Array,
    default: () => [],
  },
  stepData: {
    type: Object as PropType<TStepDataStat>,
  }
});

const emit = defineEmits(['update:step-data', 'update:requestData']);

// const stepData = useVModel(props, 'stepData', emit) as TStepDataStat;

const monacoEditRef = ref();

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
    pageSize: 200,
  },
  sqlModel: {
    env_id: null,
    source_id: null,
    sql: "",
    timeout: 0,
    variable_name: "",
  } as TSqlRequest,
  environments: [],
  requestData: {
    env_id: null,
  source_id: null,
  source_type: "mysql",
  use_type: "source",
  sql: "",
  timeout: 0,
  variable_name: "",
  }
});

// const requestData = computed({
//   get() {
//     return state.sqlModel as TSqlRequest;
//   },
//   set(val: any) {
//     state.sqlModel = val;
//   },
// });
const requestData = ref({
  env_id: null,
  source_id: null,
  source_type: "mysql",
  use_type: "source",
  sql: "",
  timeout: 0,
  variable_name: "",
})


// selectEnv
const selectEnv = (env_id: any) => {
  if (env_id) {
    state.dataSourceQuery.env_id = env_id;
    getDataSourceList();
  }
  if (state.requestData) {
    requestData.value.source_id = null;
  }
};

const getEnvList = () => {
  useEnvApi()
      .getList({ page: 1, pageSize: 1000 })
      .then((res) => {
        state.environments = res.data?.rows || [];
      });
};

// 初始化datasource
const getDataSourceList = () => {
  useEnvApi()
      .getDataSourceByEnvId(state.dataSourceQuery)
      .then((res) => {
        state.sourceList = res.data;
      });
};


const getData = () => {
  return state.requestData
};
const setData = (data: any) => {
  state.requestData = data;
  console.log(data, 'vvvvvvvvvvvvvvvvvv', state.requestData)
};

onMounted(() => {
  nextTick(() => {
    if (state.requestData!.env_id) {
      state.dataSourceQuery.env_id = state.requestData.env_id;
      getDataSourceList();
    }
    state.requestData.source_type = !state.requestData?.source_type ? 'mysql' : state.requestData?.source_type;
    state.requestData.use_type = !state.requestData?.use_type ? 'source' : state.requestData?.use_type;
  });
  getEnvList()
});

defineExpose({
  setData,
  getData
})
</script>

<style lang="scss" scoped>
.sql-request-box {
  padding: 8px;

  .sql-body {
    border: 1px solid #e6e6e6;
    border: 1px solid var(--el-border-color);
  }
}

.no-touch {
  touch-action: none;
}
</style>
