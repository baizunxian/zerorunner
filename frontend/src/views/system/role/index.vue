<template>
  <div class="system-role-container app-container">
    <el-card>
      <div class="system-user-search mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入角色名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增
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
    <SaveOrUpdateRole ref="SaveOrUpdateRoleRef" @getList="getList"/>
  </div>
</template>

<script lang="ts" setup name="SystemRole">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import SaveOrUpdateRole from '/@/views/system/role/EditRole.vue';
import {useRolesApi} from "/@/api/useSystemApi/roles";


const SaveOrUpdateRoleRef = ref();
const tableRef = ref();
const state = reactive({
  columns: [
    {
      key: 'name', label: '角色名称', width: '', align: 'center', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'role_type', label: '权限类型', width: '', align: 'center', show: true},
    {
      key: 'status', label: '角色状态', width: '', align: 'center', show: true,
      render: (row: any) => h(ElTag, {
        type: row.status == 10 ? "success" : "info",
      }, () => row.status == 10 ? "启用" : "禁用",)
    },
    {key: 'description', label: '角色描述', width: '', align: 'center', show: true},
    {key: 'description', label: '备注', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: (row: any) => h("div", null, [
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
  tableRef.value.openLoading()
  useRolesApi().getList(state.listQuery)
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
const onOpenSaveOrUpdate = (editType: string, row: any) => {
  SaveOrUpdateRoleRef.value.openDialog(editType, row);
};

// 删除角色
const deleted = (row: any) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useRolesApi().deleted({id: row.id})
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
