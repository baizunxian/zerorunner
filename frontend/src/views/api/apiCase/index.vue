<template>
  <div class="h100 app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入用例名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增</el-button>
      </div>

      <div>
        <z-table
            :columns="state.columns"
            :data="state.listData"
            v-model:page-size="state.listQuery.pageSize"
            v-model:page="state.listQuery.page"
            ref="tableRef"
            :total="state.total"
            @pagination-change="getList"
        />
      </div>
    </el-card>

    <!--    运行-->
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
        <el-form-item label="运行环境" prop="belong_project_id">
          <el-select v-model="state.runForm.env_id" placeholder="选择环境" filterable style="width:100%">
            <el-option :value="''" label="自带环境">自带环境</el-option>
            <el-option
                v-for="item in state.envList"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              <span style="float: left">{{ `${item.name}(${item.domain_name})` }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
                <span class="dialog-footer">
                  <el-button @click="state.showRunPage = !state.showRunPage">取消</el-button>
                  <el-button type="primary" :loading="state.runCaseLoading" @click="runApiTestCase">运行</el-button>
                </span>
      </template>
    </el-dialog>

    <!--    <RelationGraph></RelationGraph>-->

    <!--    关系弹窗-->
    <ApiRelationGraph ref="ApiRelationGraphRef"></ApiRelationGraph>


  </div>
</template>

<script setup name="apiCase">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElDropdown, ElDropdownItem, ElDropdownMenu, ElMessage, ElMessageBox} from 'element-plus';
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";
import {useRouter} from 'vue-router'
import {useEnvApi} from "/@/api/useAutoApi/env";
import ApiRelationGraph from "/@/components/RelationGraph/ApiRelationGraph.vue";
import {MoreFilled} from "@element-plus/icons";


const tableRef = ref();
const ApiRelationGraphRef = ref();
const router = useRouter();
const state = reactive({
  columns: [
    {key: 'id', label: 'ID', width: '55', align: 'center', show: true},
    {
      key: 'name', label: '用例名称', width: '', align: 'center', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {key: 'step_count', label: '步骤数', width: '', align: 'center', show: true},
    {key: 'remarks', label: '用例描述', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '200', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "success",
          onClick: () => {
            onOpenRunPage(row)
          }
        }, () => '运行'),

        // h(ElButton, {
        //   type: "primary",
        //   onClick: () => {
        //     onOpenSaveOrUpdate("update", row)
        //   }
        // }, () => '编辑'),

        // h(ElButton, {
        //   type: "warning",
        //   onClick: () => {
        //     toViewReport(row)
        //   }
        // }, () => '查看报告'),
        h(ElButton, {
          color: "#626aef",
          onClick: () => {
            viewRelationGraph(row)
          }
        }, () => '血缘关系'),

        // h(ElButton, {
        //   type: "danger",
        //   onClick: () => {
        //     deleted(row)
        //   }
        // }, () => '删除'),

        h(ElDropdown, {
              style: {
                verticalAlign: "middle",
                marginLeft: "12px"
              }
            },
            {
              default: () => h(ElButton, {
                style: {},
                link: true,
                icon: MoreFilled
              }),
              dropdown: () => h(ElDropdownMenu, {
                    style: {
                      minWidth: "100px"
                    },
                  },
                  {
                    default: () => [
                      h(ElDropdownItem, {
                        style: {
                          color: "var(--el-color-primary)"
                        },
                        onClick: () => {
                          onOpenSaveOrUpdate("update", row)
                        }
                      }, () => '编辑'),
                      // h(ElDropdownItem, {
                      //   style: {
                      //     color: "#626aef"
                      //   },
                      //   onClick: () => {
                      //     viewRelationGraph(row)
                      //   }
                      // }, () => '血缘关系'),
                      h(ElDropdownItem, {
                        style: {
                          color: "var(--el-color-danger)"
                        },
                        onClick: () => {
                          deleted(row)
                        }
                      }, () => '删除'),
                    ]
                  }
              )
            }
        ),
      ])
    },
  ],
  // list
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
  // run
  showRunPage: false,
  runCaseLoading: false,
  runForm: {
    id: null,
    env_id: null,
    run_type: 'suite',
  },
  //  env
  envList: []

});
// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useApiCaseApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      })
};

// 查询
const search = () => {
  state.listQuery.page = 1
  getList()
}

// 新增或修改
const onOpenSaveOrUpdate = (editType, row) => {
  let query = {}
  query.editType = editType
  if (query.editType === 'save') {
    query.timestamp = new Date().getTime()
  }
  if (row) query.id = row.id
  router.push({name: 'EditApiCase', query: query})
};

// 查看报告
const toViewReport = (row) => {
  router.push({name: 'apiReport', params: {case_id: row.id}})
}

// 删除
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useApiCaseApi().deleted({id: row.id})
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
  useEnvApi().getList({page: 1, pageSize: 1000}) // 请求数据写死，后面优化
      .then(res => {
        state.envList = res.data.rows
      })
};

//运行
const runApiTestCase = () => {
  useApiCaseApi().runSuites(state.runForm).then(res => {
    ElMessage.success(res.msg)
    state.showRunPage = false;
  })
};

const viewRelationGraph = (row) => {
  ApiRelationGraphRef.value.openDialog(row.id, 'case')
}


// 页面加载时
onMounted(() => {
  getList();
});

</script>

<style lang="scss" scoped>
:deep(.relation-draggable .el-dialog__body) {
  height: 80vh;
}
</style>