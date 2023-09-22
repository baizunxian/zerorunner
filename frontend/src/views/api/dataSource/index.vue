<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name"
                  :placeholder="`请输入数据源名称`"
                  style="max-width: 180px">
        </el-input>
        <el-button type="primary" class="ml10" @click="search">
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
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
          @selection-change="selectionChange"
          @pagination-change="getList"
      />
    </el-card>
    <EditDataSource ref="EditDataSourceRef" @getList="getList"/>
  </div>

</template>

<script setup name="ApiDataSource">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import EditDataSource from "./EditDataSource.vue";

const emit = defineEmits(["selectionChange"])

const EditDataSourceRef = ref();
const tableRef = ref();
const state = reactive({
  columns: [
    {label: '', columnType: 'selection', width: 'auto', show: true},
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {
      key: 'name', label: '数据源名称', width: 'auto', align: 'center', show: true, render: ({row}) =>
        h(ElButton, {
          link: true,
          type: "primary",
          onClick: () => {
            onOpenSaveOrUpdate("update", row)
          }
        }, () => row.name)
    },
    // {key: 'env_name', label: '所属环境', width: '', align: 'center', show: true},
    {key: 'type', label: '类型', width: '', align: 'center', show: true},
    {key: 'host', label: '地址', width: '', align: 'center', show: true},
    {key: 'port', label: '端口', width: '', align: 'center', show: true},
    {key: 'user', label: '用户名', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: ({row}) => h("div", null, [
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

//  selectionChange
  selectChangeList: []

});
// 初始化表格数据
const getList = () => {
  state.tableLoading = true
  tableRef.value.openLoading()
  useQueryDBApi().getSourceList(state.listQuery)
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

// 新增或修改角色
const onOpenSaveOrUpdate = (editType, row) => {
  EditDataSourceRef.value.openDialog(editType, row);
};

// 删除角色
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      useQueryDBApi().deletedSource({id: row.id})
        .then(() => {
          ElMessage.success('删除成功');
          getList()
        })
    })
    .catch(() => {
    });
};
const selectionChange = (val) => {
  state.selectChangeList = val
  emit("selectionChange", val)
}
const getSelectList = () => {
  return state.selectChangeList
}

defineExpose({
  getSelectList,
})

// 页面加载时
onMounted(() => {
  getList();
});
</script>
