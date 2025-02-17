<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="getList">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
          <el-icon>
            <ele-FolderAdd/>
          </el-icon>
          新增
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      />
    </el-card>
    <EditTimedTask ref="saveOrUpdateRef" @getList="getList"/>


    <el-dialog
        draggable
        v-model="state.showRunLogPage"
        width="90%"
        top="5vh"
        title="运行日志"
        destroy-on-close
        :close-on-click-modal="false">

      <TaskRecord :business_id="state.business_id" :task_type="20"></TaskRecord>

    </el-dialog>

    <!--    关系弹窗-->
    <ApiRelationGraph ref="ApiRelationGraphRef"></ApiRelationGraph>

  </div>
</template>

<script setup name="TimedTask">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElDropdown, ElDropdownItem, ElDropdownMenu, ElMessage, ElMessageBox} from 'element-plus';
import EditTimedTask from './EditTimedTask.vue';
import {useTimedTasksApi} from "/@/api/useAutoApi/timedTasks";
import {formatLookup} from "/@/utils/lookup";
import TaskRecord from "/@/views/job/taskRecord/index.vue";
import {MoreFilled} from "@element-plus/icons";
import ApiRelationGraph from "/@/components/RelationGraph/ApiRelationGraph.vue";

const saveOrUpdateRef = ref();
const ApiRelationGraphRef = ref();
const tableRef = ref();
const state = reactive({
  columns: [
    {
      key: 'name', label: '任务名称', width: '', align: 'center', show: true,
      render: ({row}) => h(ElButton, {
        type: "primary",
        link: true,
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {
      key: 'task_type',
      label: '调度模式',
      width: '',
      align: 'center',
      show: true,
      render: ({row}) => handleTaskType(row)
    },
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {
      key: 'enabled',
      label: '任务状态',
      width: '',
      align: 'center',
      show: true,
      render: ({row}) => {
        let value = formatLookup("api_timed_task_status", row.enabled)
        return h("span", {style: {color: row.enabled ? '#0cbb52' : '#e6a23c'}}, value)
      }
    },
    {key: 'description', label: '任务描述', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '250', align: 'center',
      render: ({row}) => h("div", null, [

        h(ElButton, {
          type: "",
          color: "#626aef",
          onClick: () => {
            runOnceJob(row)
          }
        }, () => "手动执行"),

        h(ElButton, {
          type: "success",
          onClick: () => {
            taskSwitch(row)
          }
        }, () => row.enabled ? '停止' : '启动'),
        h(ElButton, {
          type: "warning",
          onClick: () => {
            viewRunLog(row)
          }
        }, () => "日志"),

        // h(ElButton, {
        //   type: "primary",
        //   onClick: () => {
        //     onOpenSaveOrUpdate("update", row)
        //   }
        // }, () => '编辑'),

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
                      h(ElDropdownItem, {
                        style: {
                          color: "#626aef"
                        },
                        onClick: () => {
                          viewRelationGraph(row)
                        }
                      }, () => '血缘关系'),
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
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },

  // 日志
  showRunLogPage: false,
  business_id: '',
});
// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useTimedTasksApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      })
};

// 新增或修改
const onOpenSaveOrUpdate = (editType, row) => {
  saveOrUpdateRef.value.openDialog(editType, row);
};

// 新增或修改
const taskSwitch = (row) => {
  ElMessageBox.confirm(`${row.enabled ? '停止' : '启动'}当前任务, 是否继续?`, '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    useTimedTasksApi().taskSwitch({id: row.id})
        .then(() => {
          ElMessage.success('操作成功！');
          getList()
        })
  })

};

// 删除
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useTimedTasksApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

const runOnceJob = (row) => {
  ElMessageBox.confirm("即将手动调度任务, 是否继续？", '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    useTimedTasksApi().runOnceJob({id: row.id}).then(() => {
      ElMessage.success("执行成功！")
    })
  })
}

const handleTaskType = (row) => {
  if (row.task_type === 'crontab') {
    return `${row.task_type}[${row.crontab}]`
  } else if (row.task_type === 'interval') {
    return `${row.task_type}[${row.interval_every} ${row.interval_period}]`;
  }
}

const viewRelationGraph = (row) => {
  ApiRelationGraphRef.value.openDialog(row.id, 'timed_task')
}

const viewRunLog = (row) => {
  state.business_id = row.id
  state.showRunLogPage = true
}

// 页面加载时
onMounted(() => {
  getList();
});

</script>

<style>

.stop {
  background-color: #c1bfc7;
}

.start {
  background-color: #0cbb52;
}

.request-editor-tabs-badge {
  display: inline-flex;
  width: 8px;
  height: 8px;
  margin-right: 5px;
  border-radius: 8px;
}
</style>