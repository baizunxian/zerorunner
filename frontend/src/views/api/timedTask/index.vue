<template>
  <div>
    <el-card>
      <div class="mb15">
        <el-input v-model="listQuery.name" placeholder="请输入名称" style="max-width: 180px"></el-input>
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
      <zero-table
          :columns="columns"
          :data="listData"
          v-model:page-size="listQuery.pageSize"
          v-model:page="listQuery.page"
          :total="total"
          @pagination-change="getList"
      />
    </el-card>
    <save-or-update ref="saveOrUpdateRef" @getList="getList"/>
  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import saveOrUpdate from '/@/views/api/timedTask/components/saveOrUpdate.vue';
import {useTimedTasksApi} from "/@/api/useAutoApi/timedTasks";
import {formatLookup} from "/@/utils/lookup";

export default defineComponent({
  name: 'apiTimedTask',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
    const state = reactive({
      columns: [
        {key: 'name', label: '任务名称', width: '', align: 'center', show: true},
        {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
        {key: 'crontab_str', label: '执行时间', width: '', align: 'center', show: true},
        {
          key: 'run_type',
          label: '任务类型',
          width: '',
          align: 'center',
          show: true,
          lookupCode: 'api_report_run_type'
        },
        {
          key: 'enabled',
          label: '任务状态',
          width: '',
          align: 'center',
          show: true,
          lookupCode: 'api_timed_task_status',
        },
        {key: 'description', label: '备注', width: '', align: 'center', show: true},
        {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
        {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
        {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
        {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
        {
          label: '操作', columnType: 'string', fixed: 'right', width: 'auto',
          render: (row: any) => h("div", null, [
            h(ElButton, {
              type: "success",
              onClick: () => {
                taskSwitch(row)
              }
            }, () => row.enabled ? '停止' : '启动'),

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
      // list
      listData: [],
      tableLoading: false,
      total: 0,
      listQuery: {
        page: 1,
        pageSize: 20,
        name: '',
      },
    });
    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useTimedTasksApi().getList(state.listQuery)
          .then(res => {
            state.listData = res.data.rows
            state.total = res.data.rowTotal
            state.tableLoading = false
          })
    };

    // 新增或修改
    const onOpenSaveOrUpdate = (editType: string, row: any) => {
      saveOrUpdateRef.value.openDialog(editType, row);
    };

    // 新增或修改
    const taskSwitch = (row: any) => {
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

    // 删除角色
    const deleted = (row: any) => {
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
    // 页面加载时
    onMounted(() => {
      getList();
    });
    return {
      getList,
      saveOrUpdateRef,
      onOpenSaveOrUpdate,
      deleted,
      taskSwitch,
      formatLookup,
      ...toRefs(state),
    };
  },
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