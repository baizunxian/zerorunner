<template>
  <div class="" style="padding: 10px">
    <el-card style="overflow: auto">
      <z-splitpanes class="default-theme">
        <z-pane :size="20">
          <div style="padding: 10px">
            <div>
              <!--              <el-input type="text" size="default" v-model="moduleQuery.name"></el-input>-->
              <!--              <el-button type="primary" class="ml10" @click="getList">-->
              <!--                -->
              <!--                <el-icon>-->
              <!--                  <ele-Search/>-->
              <!--                </el-icon>-->
              <!--                查询-->
              <!--              </el-button>-->
              <el-button type="primary" size="default">
                添加模块
              </el-button>
              <el-button type="primary" size="default" @click="onOpenSaveOrUpdate('save', null)">
                添加接口
              </el-button>
              <el-button type="warning" size="default" @click="getModuleList">
                刷新
              </el-button>
              <!--              <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">-->
              <!--                <el-icon>-->
              <!--                  <ele-FolderAdd/>-->
              <!--                </el-icon>-->
              <!--                新增-->
              <!--              </el-button>-->

            </div>
            <el-divider style="margin: 10px 0 5px 0;"/>
            <el-collapse v-model="activeModule" accordion @change="moduleChange">
              <el-collapse-item v-for="module in moduleList" :name="module.id" :key="module.id">

                <template #title>
                  <div>
                    <div>
                      <span style="font-weight: 600; color: #3068a3">[{{ module.project_name }}]{{ module.name }}</span>
                    </div>
                    <div>

                    </div>
                  </div>
                </template>

                <el-table
                    :id="`moduleList_${module.id}`"
                    :show-header="false"
                    :data="module.caseList"
                    highlight-current-row
                    style="width: 100%"
                    @row-click="caseClick"
                >
                  <el-table-column property="name" label="Name" width="auto">
                    <template #default="{ row }">
                      <el-tag :style="{background: getMethodColor(row.method), color: '#ffffff'}"
                              style="margin-right: 10px"
                      >{{ row.method }}
                      </el-tag>
                      <span>{{ row.name }}</span>
                    </template>
                    <!--                <template #header>-->
                    <!--                  <el-input v-model="search" size="small" placeholder="Type to search"/>-->
                    <!--                </template>-->
                  </el-table-column>
                </el-table>


              </el-collapse-item>
            </el-collapse>
          </div>
        </z-pane>
        <z-pane :size="80">
          <!--        <el-card>-->
          <!--          <div class="mb8">-->
          <!--            <div>-->
          <!--              <el-input v-model="listQuery.name" placeholder="请输入用例名称" style="max-width: 180px"></el-input>-->
          <!--              <el-button type="primary" class="ml10" @click="getList">-->
          <!--                <el-icon>-->
          <!--                  <ele-Search/>-->
          <!--                </el-icon>-->
          <!--                查询-->
          <!--              </el-button>-->
          <!--              <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">-->
          <!--                <el-icon>-->
          <!--                  <ele-FolderAdd/>-->
          <!--                </el-icon>-->
          <!--                新增-->
          <!--              </el-button>-->
          <!--            </div>-->
          <!--          </div>-->
          <!--          <div class="mb8">-->
          <!--            <el-button type="primary" link class="" @click="openImportPage">-->
          <!--              <el-icon>-->
          <!--                <ele-FolderAdd/>-->
          <!--              </el-icon>-->
          <!--              导入-->
          <!--            </el-button>-->
          <!--          </div>-->
          <!--          <z-table-->
          <!--              :columns="columns"-->
          <!--              :data="listData"-->
          <!--              v-model:page-size="listQuery.pageSize"-->
          <!--              v-model:page="listQuery.page"-->
          <!--              :total="total"-->
          <!--              @pagination-change="getList"-->
          <!--              @selection-change="selectionChange"-->
          <!--          >-->
          <!--          </z-table>-->
          <!--        </el-card>-->
          <div style="padding: 10px">
            <save-or-update :api_id="activeCaseId" @moduleChange="moduleChange"></save-or-update>
          </div>


        </z-pane>
      </z-splitpanes>

      <!--    运行用例-->
      <el-dialog
          draggable
          v-model="showRunPage"
          width="600px"
          top="8vh"
          title="运行用例"
          :close-on-click-modal="false">
        <el-form
            :model="runForm"
            label-width="70px"

        >
          <el-form-item label="运行模式" prop="run_mode">
            <el-select v-model="runForm.run_type" placeholder="选择运行模式" filterable style="width:100%">
              <el-option :value="10" label="同步运行(同步执行,等待执行结果)"></el-option>
              <el-option :value="20" label="异步运行(异步执行用例,后台运行,执行结束后报告列表查看)"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="运行环境" prop="base_url">
            <el-select v-model="runForm.base_url" placeholder="选择环境" filterable style="width:100%">
              <el-option :value="''" label="自带环境">自带环境</el-option>
              <el-option
                  v-for="item in envList"
                  :key="item.id"
                  :label="item.name"
                  :value="item.url">
                <span style="float: left">{{ item.name }}</span>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
              <el-button @click="showRunPage = !showRunPage">取消</el-button>
              <el-button type="primary" :loading="runCaseLoading" @click="runTestCase">运行</el-button>
            </span>
        </template>
      </el-dialog>

      <!--    测试报告-->

      <report-detail :report-info="reportInfo" ref="reportDetailRef"/>

      <!--    postman 导入 import-->
      <el-dialog
          draggable
          v-model="showImportPage"
          width="600px"
          top="8vh"
          title="导入"
          :close-on-click-modal="false">

        <el-form
            :rules="importRules"
            ref="importFormRef"
            :model="importForm"
            label-width="80px"
        >

          <el-form-item label="所属项目" prop="project_id">
            <el-select
                v-model="importForm.project_id" placeholder="选择归属项目"
                clearable
                filterable
                style="width: 100%;" @change="selectProject">
              <el-option
                  v-for="project in projectList"
                  :key="project.id"
                  :label="project.name"
                  :value="project.id">
                {{ project.name }}
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属模块" prop="module_id">
            <el-select
                v-model="importForm.module_id"
                placeholder="选择模块"
                filterable style="width: 100%;"
            >
              <el-option
                  v-for="modules in moduleList"
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
                <input size="small" type="file" id="selectFile" @change="fileChange($event)"
                       class="file-input__native">

                <el-button v-if="!importForm.file_info.raw" type="info" size="small" @click="selectFile()">选择文件
                </el-button>
                <div v-else class="file-input__name">
                  <div class="file-input__name__title" :title="importForm.file_info.name">{{
                      importForm.file_info.name
                    }}
                  </div>
                  <el-button class="file-input__name__delete-icon" size="small" type="primary" link
                             @click="deletedFile">
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
          <el-button @click="showImportPage = false">取消</el-button>
          <el-button type="primary" @click="submitUpload" :loading="importButtonStart">导入</el-button>
        </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
// import saveOrUpdate from '/@/views/api/module/components/saveOrUpdate.vue';
import {useApiInfoApi} from "/@/api/useAutoApi/apiInfo";
import {useRouter} from "vue-router";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {useModuleApi} from "/@/api/useAutoApi/module";
import {useProjectApi} from "/@/api/useAutoApi/project";
import {ElTag} from "element-plus"
import {getMethodColor} from "/@/utils/case";
import reportDetail from "/@/components/Z-Report/ApiReport/ReportInfo/ReportDetail.vue";
import saveOrUpdate from "/@/views/api/apiInfo/components/EditApi.vue";


export default defineComponent({
  name: 'apiTestCase',
  components: {
    // saveOrUpdate,
    reportDetail,
    saveOrUpdate,
  },
  setup() {
    const reportDetailRef = ref();
    const importFormRef = ref();
    const uploadRef = ref();
    const moduleListRef = ref();
    const router = useRouter();
    const state = reactive({
      columns: [
        // {label: '序号', columnType: 'selection', width: 'auto', show: true},
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
          label: '操作', fixed: 'right', width: '140', align: 'center',
          render: ({row}) => h("div", null, [
            h(ElButton, {
              link: true,
              type: "primary",
              onClick: () => {
                onOpenRunPage(row)
              }
            }, () => '运行'),

            h(ElButton, {
              link: true,
              type: "primary",
              onClick: () => {
                onOpenSaveOrUpdate("update", row)
              }
            }, () => '编辑'),

            h(ElButton, {
              link: true,
              type: "primary",
              onClick: () => {
                deleted(row)
              }
            }, () => '删除')
          ])
        },
      ],

      //activeModule

      activeModule: "",

      activeCaseId: null,


      listData: [],
      tableLoading: false,
      total: 0,
      listQuery: {
        page: 1,
        pageSize: 20,
        name: '',
      },
      selectionData: [],
      // run test apiInfo
      showRunPage: false,
      runCaseLoading: false,
      envList: [],
      runForm: {
        id: null,
        base_url: '',
        run_type: 10,
        run_mode: "case",
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
    });

    // moduleChange

    const moduleChange = async (module_id) => {
      if (module_id) {
        let moduleInfo = state.moduleList.find((m) => m.id === module_id)
        if (moduleInfo) {
          let listQuery = {
            page: 1,
            pageSize: 20,
            module_id: module_id,
            name: '',
          }
          let res = await useApiInfoApi().getList(listQuery)
          moduleInfo.caseList = res.data.rows
        }
      }
    }

    // caseClick
    const caseClick = (row) => {
      state.activeCaseId = row.id
    }

    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useApiInfoApi().getList(state.listQuery)
          .then(res => {
            state.listData = res.data.rows
            state.total = res.data.rowTotal
            state.tableLoading = false
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
      state.activeCaseId = null
      if (row) state.activeCaseId = row.id
      let moduleListRef = document.getElementById(`moduleList_${state.activeModule}`)
      if (moduleListRef) {
        console.log("moduleListRef---<", moduleListRef)
      }

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
      state.runForm.id = row.id;
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
    const runTestCase = () => {
      state.runCaseLoading = !state.runCaseLoading;
      useApiInfoApi().run(state.runForm)
          .then((res) => {
            if (state.runForm.run_mode === 1) {
              ElMessage.success('运行成功');
              state.reportInfo = res.data
              state.runCaseLoading = !state.runCaseLoading;
              reportDetailRef.value.showReport()
            } else {
              ElMessage.success(res.msg);
              state.runCaseLoading = !state.runCaseLoading;
            }

          })
          .catch((err) => {
            ElMessage.error(err.message);
            state.runCaseLoading = !state.runCaseLoading;
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
            if (state.activeModule) {
              moduleChange(state.activeModule)
            }
          })
    }

    // 文件上传
    const submitUpload = () => {
      state.importButtonStart = true
      importFormRef.value.validate(async (vai) => {
        if (vai) {
          if (!state.importForm.file_info.raw) {
            ElMessage.info('请选择上传文件！')
            state.importButtonStart = false
            return
          }
          try {
            let formData = new FormData()
            formData.append('file', state.importForm.file_info.raw)
            formData.append('project_id', state.importForm.project_id)
            formData.append('module_id', state.importForm.module_id)
            let res = await useApiInfoApi().postman2case(formData)
            ElMessage.success(`成功导入${res.data}条用例！`)
            state.importButtonStart = false
            state.showImportPage = false
            getList()

            // useTestCaseApi().postman2case(formData)
            //     .then((res: any) => {
            //       ElMessage.success(`成功导入${res.data}条用例！`)
            //       state.importButtonStart = false
            //       state.showImportPage = false
            //       getList()
            //     })
          } catch (e) {
            state.importButtonStart = false
          }
        } else {
          state.importButtonStart = false
        }
      })
    }

    // 选择文件时触发，上传文件，回写地址
    const fileChange = (e) => {
      let file = e.target.files[0]
      state.importForm.file_info.raw = file
      state.importForm.file_info.name = file.name
    }
    // 删除文件处理
    const deletedFile = () => {
      let fileRef = document.getElementById('selectFile')
      if (fileRef) fileRef.value = ''
      state.importForm.file_info.raw = ''
      state.importForm.file_info.name = ''
    }

    // 选择文件
    const selectFile = () => {
      let fileRef = document.getElementById('selectFile')
      if (fileRef) fileRef.click()
    }

    // // 获取请求方式tag颜色
    // const getMethodColor = (method: string) => {
    //   let color = ""
    //   if (method == "GET") {
    //     color = "#61affe"
    //   } else if (method == "POST") {
    //     color = "#49cc90"
    //   } else if (method == "DELETE") {
    //     color = "#f93e3d"
    //   } else if (method == "PUT") {
    //     color = "#fca130"
    //   }
    //   return color
    // }

    // 页面加载时
    onMounted(() => {
      getList();
      getModuleList()
    });
    return {
      moduleChange,
      caseClick,
      getList,
      moduleListRef,
      reportDetailRef,
      importFormRef,
      uploadRef,
      getEnvList,
      onOpenRunPage,
      runTestCase,
      onOpenSaveOrUpdate,
      deleted,
      router,
      fileChange,
      deletedFile,
      selectFile,
      openImportPage,
      getProjectList,
      selectProject,
      getModuleList,
      submitUpload,
      selectionChange,
      getSelectionData,
      getMethodColor,
      ...toRefs(state),
    };
  },
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

:deep(.el-card) {
  border-radius: 10px;
}

:deep(.el-card__body) {
  padding: 0;
}

:deep(.el-tag) {
  --el-tag-border-color: #FFFFFF00
}

:deep(.el-table__row>td) {
  border: none;
}

:deep(.el-table::before) {
  height: 0px;
}

:deep(.el-table__inner-wrapper::before) {
  background-color: rgb(0, 0, 0, 0);
}

:deep(.el-collapse) {
  --el-collapse-border-color: #fffff;
}

:deep(.el-table__body tr.current-row>td.el-table__cell) {
  //border-radius: 4px;
  border-left: 2px solid #409eff !important;
  margin-bottom: 20px;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
}
</style>