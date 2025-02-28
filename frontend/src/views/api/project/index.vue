<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入项目名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          ref="tableRef"
          :data="state.listData"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      >
      </z-table>
    </el-card>
    <Edit ref="EditRef" @getList="getList"/>
  </div>
</template>

<script setup name="apiProject">
import {defineAsyncComponent, h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useProjectApi} from "/@/api/useAutoApi/project";

// 引入组件
const Edit = defineAsyncComponent(() => import("./EditProject.vue"))

// 自定义数据
const tableRef = ref();
const EditRef = ref();
const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
    {
      key: 'name', label: '项目名称', align: 'center', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'responsible_name', label: '负责人', align: 'center', width: '', show: true},
    {key: 'test_user', label: '测试人员', align: 'center', width: '', show: true},
    {key: 'dev_user', label: '开发人员', align: 'center', width: '', show: true},
    {key: 'publish_app', label: '发布应用', align: 'center', width: '', show: true},
    {key: 'simple_desc', label: '描述', align: 'center', width: '', show: true},
    {key: 'remarks', label: '备注', align: 'center', width: '', show: true},
    {key: 'config_id', label: '关联配置', align: 'center', width: '', show: true},
    {key: 'updation_date', label: '更新时间', align: 'center', width: '150', show: true},
    {key: 'updated_by_name', label: '更新人', align: 'center', width: '', show: true},
    {key: 'creation_date', label: '创建时间', align: 'center', width: '150', show: true},
    {key: 'created_by_name', label: '创建人', align: 'center', width: '', show: true},
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
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
});

// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useProjectApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
        tableRef.value.closeLoading()
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
  EditRef.value.openDialog(editType, row);
};

// 删除角色
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useProjectApi().deleted({id: row.id})
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

</script>
