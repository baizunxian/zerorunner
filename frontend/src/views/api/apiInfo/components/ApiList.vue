<template>
  <div class="app-container">
    <el-card>
      <div class="mb8">
        <div>
          <el-input v-model="state.listQuery.name" placeholder="请输入用例名称" style="max-width: 180px"></el-input>
          <el-button type="primary" class="ml10" @click="getList">查询
          </el-button>
          <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增
          </el-button>
        </div>
      </div>

      <!--      <div class="mb8">-->
      <!--        <el-button type="primary" link class="" @click="openImportPage">-->
      <!--          <el-icon>-->
      <!--            <ele-FolderAdd/>-->
      <!--          </el-icon>-->
      <!--          导入-->
      <!--        </el-button>-->
      <!--      </div>-->
      <!--      -->
      <!--       tool      -->
      <div class="mb8 mt8">
        <el-checkbox v-model="state.oneSelf" @change="oneSelfChange">
          只看自己创建
        </el-checkbox>


        <el-button type="primary"
                   link
                   class="ml5"
                   :disabled="state.selectionData.length === 0"
                   style="vertical-align: text-bottom"
                   @click="onOpenBatchRunPage">
          <el-icon>
            <ele-CaretRight/>
          </el-icon>
          批量执行
        </el-button>

      </div>
      <!--      list    -->
      <div>
        <z-table
            :columns="state.columns"
            :data="state.listData"
            ref="tableRef"
            v-model:page-size="state.listQuery.pageSize"
            v-model:page="state.listQuery.page"
            :total="state.total"
            @pagination-change="getList"
            @selection-change="selectionChange"
        >
        </z-table>
      </div>
    </el-card>
    <!--    运行用例-->
    <el-dialog
        draggable
        v-model="state.showRunPage"
        width="600px"
        top="8vh"
        title="运行用例"
        :close-on-click-modal="false">
      <el-form
          :model="state.runForm"
          label-width="70px"

      >
        <el-form-item label="运行模式" prop="run_mode">
          <el-select v-model="state.runForm.run_mode" placeholder="选择运行模式" filterable style="width:100%">
            <el-option :value="10" label="同步运行(同步执行,等待执行结果)"></el-option>
            <el-option :value="20" label="异步运行(异步执行用例,后台运行,执行结束后报告列表查看)"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="运行环境" prop="base_url">
          <el-select v-model="state.runForm.env_id" placeholder="选择环境" filterable style="width:100%">
            <el-option :value="0" label="自带环境">自带环境</el-option>
            <el-option
                v-for="item in state.envList"
                :key="item.id"
                :label="`${item.name}(${item.domain_name})`"
                :value="item.id">
              <span style="float: left">{{ `${item.name}(${item.domain_name})` }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
            <span class="dialog-footer">
              <el-button @click="state.showRunPage = !state.showRunPage">取 消</el-button>
              <el-button type="primary" :loading="state.runApiLoading" @click="runApi">运 行</el-button>
            </span>
      </template>
    </el-dialog>

    <!--    测试报告-->
    <ReportDetail :report-info="state.reportInfo" ref="reportDetailRef"/>

    <!--    postman 导入 import-->
    <el-dialog
        draggable
        v-model="state.showImportPage"
        width="600px"
        top="8vh"
        title="导入"
        :close-on-click-modal="false">

      <el-form
          :rules="state.importRules"
          ref="importFormRef"
          :model="state.importForm"
          label-width="80px"
      >

        <el-form-item label="所属项目" prop="project_id">
          <el-select
              v-model="state.importForm.project_id" placeholder="选择归属项目"
              clearable
              filterable
              style="width: 100%;" @change="selectProject">
            <el-option
                v-for="project in state.projectList"
                :key="project.id"
                :label="project.name"
                :value="project.id">
              {{ project.name }}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属模块" prop="module_id">
          <el-select
              v-model="state.importForm.module_id"
              placeholder="选择模块"
              filterable style="width: 100%;"
          >
            <el-option
                v-for="modules in state.moduleList"
                :key="modules.id"
                :label="modules.name"
                :value="modules.id">
              {{ modules.name }}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上传文件">
          <div class="file-input-container">
            <div class="file-input">
              <input size="small" type="file" id="selectFile" @change="state.fileChange($event)"
                     class="file-input__native">

              <el-button v-if="!state.importForm.file_info.raw" type="info" size="small" @click="state.selectFile()">
                选择文件
              </el-button>
              <div v-else class="file-input__name">
                <div class="file-input__name__title" :title="state.importForm.file_info.name">
                  {{ state.importForm.file_info.name }}
                </div>
                <el-button class="file-input__name__delete-icon" size="small" type="primary" link
                           @click="state.deletedFile">
                  <el-icon>
                    <ele-Close/>
                  </el-icon>
                </el-button>
              </div>
            </div>
            <span>目前只支持postman json文件</span>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.showImportPage = false">取消</el-button>
          <el-button type="primary" @click="state.submitUpload" :loading="state.importButtonStart">导入</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="apiInfoList">
import {defineAsyncComponent, h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import {useApiInfoApi} from "/@/api/useAutoApi/apiInfo";
import {useRouter} from "vue-router";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {useModuleApi} from "/@/api/useAutoApi/module";
import {useProjectApi} from "/@/api/useAutoApi/project";
import {getMethodColor} from "/@/utils/case";
import {useUserInfo} from '/@/stores/userInfo';

const userInfoStore = useUserInfo()

const ReportDetail = defineAsyncComponent(() => import("/@/components/Z-Report/ApiReport/ReportInfo/ReportDetail.vue"))

const reportDetailRef = ref();
const importFormRef = ref();
const tableRef = ref();
const router = useRouter();

const state = reactive({
  columns: [
    {label: '', columnType: 'selection', width: 'auto', show: true},
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {key: 'id', label: 'ID', columnType: 'string', width: 'auto', show: true},
    {
      key: 'name', label: '用例名', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {
      key: 'method', label: '请求方式', width: '', show: true,
      render: ({row}) => h(ElTag, {
        type: "",
        style: {"background": getMethodColor(row.method), color: "#ffffff",}
      }, () => row.method)
    },
    {key: 'url', label: '请求地址', width: 'auto', show: true},
    {key: 'project_name', label: '所属项目', width: 'auto', show: true},
    {key: 'module_name', label: '所属模块', width: 'auto', show: true},
    {key: 'config_id', label: '关联配置', width: 'auto', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', show: true},
    {key: 'updated_by_name', label: '更新人', width: 'auto', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', show: true},
    {key: 'created_by_name', label: '创建人', width: 'auto', show: true},
    {
      label: '操作', fixed: 'right', width: '200', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "success",
          onClick: () => {
            onOpenRunPage(row)
          }
        }, () => '运行'),

        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenSaveOrUpdate("update", row)
          }
        }, () => '编辑'),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deleted(row)
          }
        }, () => '删除')
      ])
    },
  ],

  listData: [],
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
    created_by: null,
  },
  selectionData: [],
  // run test apiInfo
  showRunPage: false,
  runApiLoading: false,
  envList: [],
  runForm: {
    id: null,
    ids: [],
    env_id: null,
    run_type: "api",
    run_mode: 10,
    api_run_mode: "one",  // one, batch
  },
  // report
  reportInfo: {},

  //project
  projectList: [],
  projectQuery: {
    page: 1,
    pageSize: 1000,
  },
  //module
  moduleList: [],
  moduleQuery: {
    page: 1,
    pageSize: 1000,
    name: '',
    project_id: null
  },

  // import
  showImportPage: false,
  importButtonStart: false,
  importForm: {
    file_info: {
      raw: '',
      name: '',
    },
    project_id: '',
    module_id: '',
  },
  importRules: {
    project_id: [{required: true, message: '请选择项目', trigger: 'blur'}],
    module_id: [{required: true, message: '请选择模块', trigger: 'blur'}],
  },
  // oneSelf
  oneSelf: false,
});


// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useApiInfoApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
        tableRef.value.closeLoading()
      }).catch(() => {
    tableRef.value.closeLoading()
  })
};

// 选择用例
const selectionChange = (val) => {
  state.selectionData = val
}
// 获取选中用例
const getSelectionData = () => {
  return state.selectionData
}
// 新增或修改
const onOpenSaveOrUpdate = (editType, row) => {
  let query = {}
  query.editType = editType
  if (row) query.id = row.id
  router.push({name: 'EditApiInfo', query: query})

};

// 删除
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useApiInfoApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

// 打开运行页面
const onOpenRunPage = (row) => {
  state.showRunPage = true;
  state.runForm.api_run_mode = 'one'
  state.runForm.id = row.id;
  getEnvList();
};

// 打开运行页面
const onOpenBatchRunPage = () => {
  state.showRunPage = true;
  state.runForm.api_run_mode = 'batch'
  state.runForm.ids = state.selectionData.map((item) => item.id);
  getEnvList();
};
// 获取环境信息
const getEnvList = () => {
  useEnvApi().getList({page: 1, pageSize: 1000})  // 请求数据写死，后面优化
      .then(res => {
        state.envList = res.data.rows
      })
}
// 运行测试用例
const runApi = () => {
  state.runApiLoading = !state.runApiLoading;
  useApiInfoApi().runApi(state.runForm)
      .then((res) => {
        if (state.runForm.run_mode === 10 && state.runForm.api_run_mode === 'one') {
          ElMessage.success('运行成功');
          state.reportInfo = res.data
          reportDetailRef.value.showReport()
          state.showRunPage = !state.showRunPage;
        } else {
          ElMessage.success("执行成功~");
          state.showRunPage = !state.showRunPage;
        }
        state.runApiLoading = !state.runApiLoading;
      })
      .catch((err) => {
        ElMessage.error(err.message);
        state.runApiLoading = !state.runApiLoading;
      })
}

// import
//  ----------------project start-------------------------------------

// show import page
const openImportPage = () => {
  state.showImportPage = !state.showImportPage
  state.importForm.project_id = ''
  state.importForm.module_id = ''
  state.importForm.file_info.raw = ''
  state.importForm.file_info.name = ''
  getProjectList()
}
// 获取项目列表
const getProjectList = () => {
  useProjectApi().getList(state.projectQuery) // 请求数据写死，后面优化
      .then(res => {
        state.projectList = res.data.rows
      })
}
// 选择项目
const selectProject = (project_id) => {
  state.moduleQuery.project_id = project_id
  state.moduleList = []
  state.importForm.module_id = ''
  getModuleList()
}

//  ----------------module start-------------------------------------
// 获取模块列表
const getModuleList = () => {
  useModuleApi().getList(state.moduleQuery) // 请求数据写死，后面优化
      .then(res => {
        state.moduleList = res.data.rows
      })
}

// 只看自己
const oneSelfChange = (val) => {
  state.listQuery.created_by = val ? userInfoStore.userInfos.id : null
  getList()
}

defineExpose({
  getSelectionData,
})

// 页面加载时
onMounted(() => {
  getList();
  getModuleList()
});

</script>

<style lang="scss" scoped>
.file-input-container {
  display: inline-block;
  max-width: 100%;

  .file-input {
    display: flex;
    align-items: center;
    padding: var(--spacing-xs);

    .file-input__native {
      opacity: 0;
      position: absolute;
      width: 0;
      height: 0;
      pointer-events: none;
    }

    .file-input__fake {
      position: relative;
      height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;
      background-color: #F2F2F2;
      min-width: 100px;
      color: #6B6B6B;
      font-weight: 600;

      &:hover {
        color: #212121;
        background-color: #E6E6EE;
      }
    }

    .btn {
      box-sizing: border-box;
      border-radius: 4px;
    }

    .file-input__name {
      box-sizing: border-box;
      display: flex;
      min-width: 0;
      height: 24px;
      align-items: center;
      border-radius: 4px;
      border: 1px solid #E6E6E6;
      font-size: 12px;
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica, Arial, sans-serif;
      color: #212121;
      background-color: transparent;
      padding: 4px 2px;

      .file-input__name__title {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .file-input__name__delete-icon {
        display: flex;
        align-items: center;
        margin-left: 8px;
        padding-right: 2px;
        cursor: pointer;
        color: #212121;
      }
    }
  }
}

</style>