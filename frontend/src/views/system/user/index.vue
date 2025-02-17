<template>
  <div class="system-user-container app-container">
    <el-card>
      <div class="system-user-search mb15">
        <el-input v-model="state.listQuery.username" placeholder="请输入用户名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
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
          @pagination-change="getList"
      />
    </el-card>
    <SaveOrUpdateUser @getList="getList" :roleList="state.roleList" ref="SaveOrUpdateUserRef"/>
  </div>
</template>

<script setup name="SystemUser">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import SaveOrUpdateUser from '/@/views/system/user/EditUser.vue';
import {useUserApi} from '/@/api/useSystemApi/user';
import {useRolesApi} from "/@/api/useSystemApi/roles";

const SaveOrUpdateUserRef = ref()
const tableRef = ref()

const state = reactive({
  columns: [
    {
      key: 'username', label: '账户名称', width: '', align: 'center', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.username)
    },
    {key: 'nickname', label: '用户昵称', width: '', align: 'center', show: true},
    {
      key: 'roles', label: '关联角色', width: '', align: 'center', show: true,
      render: ({row}) => handleRoles(row.roles)
    },
    {key: 'email', label: '邮箱', width: '', align: 'center', show: true},
    {
      key: 'status', label: '用户状态', width: '', align: 'center', show: true,
      render: ({row}) => h(ElTag, {
        type: row.status ? "success" : "info",
      }, () => row.status ? "启用" : "禁用",)
    },
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
  ],
  // list
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    username: '',
  },
  //rule
  roleList: [],
  roleQuery: {
    page: 1,
    pageSize: 100,
  }
});
// 获取用户数据
const getList = () => {
  tableRef.value.openLoading()
  useUserApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      })
};

const getRolesList = () => {
  useRolesApi().getList(state.roleQuery)
      .then((res) => {
        state.roleList = res.data.rows
      })
};

// 查询
const search = () => {
  state.listQuery.page = 1
  getList()
}

// 新增或修改用户
const onOpenSaveOrUpdate = (editType, row) => {
  SaveOrUpdateUserRef.value.openDialog(editType, row);
};

// 删除用户
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useUserApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

// 处理角色名称
const handleRoles = (roles) => {
  let roleTagList = []
  roles = roles ? roles : []
  roles.forEach((role) => {
    let roleName = state.roleList.find(e => e.id == role)?.name
    roleTagList.push(h(ElTag, null, () => roleName))
  })
  return h('div', null, roleTagList)
}
// 页面加载时
onMounted(() => {
  getList();
  getRolesList()
});

</script>
