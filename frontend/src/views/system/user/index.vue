<template>
  <div class="system-user-container">
    <el-card shadow="hover">
      <div class="system-user-search mb15">
        <el-input v-model="listQuery.username" placeholder="请输入用户名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
          <el-icon>
            <ele-FolderAdd/>
          </el-icon>
          新增用户
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
    <save-or-update @getList="getList" :roleList="roleList" ref="saveOrUpdateRef"/>
  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import saveOrUpdate from '/@/views/system/user/components/saveOrUpdate.vue';
import {useUserApi} from '/@/api/useSystemApi/user';
import {useStore} from "/@/store";
import {useRolesApi} from "/@/api/useSystemApi/roles";

// 定义接口来定义对象的类型
interface TableDataRow {
  id: number;
  username: string;
  email: string;
  roles: string;
  status: boolean;
  nickname: string;
  user_type: number;
  created_by: number;
  updated_by: number;
  creation_date: string;
  updation_date: string;
}

interface listQueryRow {
  page: number;
  pageSize: number;
  username: string;

}

interface StateRow {
  fieldData: Array<any>;
  listData: Array<TableDataRow>;
  tableLoading: boolean;
  total: number;
  listQuery: listQueryRow;
  roleList: Array<any>;
  roleQuery: listQueryRow;
}


export default defineComponent({
  name: 'systemUser',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
    const store = useStore();
    const userInfos = store.state.userInfos.userInfos;
    const state = reactive<StateRow>({
      columns: [
        {
          key: 'username', label: '账户名称', width: '', align: 'center', showTooltip: true,
          render: (row: any) => h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenSaveOrUpdate("update", row)
            }
          }, row.username)
        },
        {key: 'nickname', label: '用户昵称', width: '', align: 'center', showTooltip: true},
        {
          key: 'roles', label: '关联角色', width: '', align: 'center', showTooltip: true,
          render: (row: any) => handleRoles(row.roles)
        },
        {key: 'email', label: '邮箱', width: '', align: 'center', showTooltip: true},
        {key: 'status', label: '用户状态', width: '', align: 'center', showTooltip: true,
          render: (row: any) => h(ElTag, {
            type: row.status ? "success" : "info",
          }, row.status ? "启用" : "禁用",)},
        {key: 'remarks', label: '备注', width: '', align: 'center', showTooltip: true},
        // {key: 'updation_date', label: '更新时间', width: '150', align: 'center', showTooltip: true},
        // {key: 'updated_by_name', label: '更新人', width: '', align: 'center', showTooltip: true},
        {key: 'creation_date', label: '创建时间', width: '150', align: 'center', showTooltip: true},
        // {key: 'created_by_name', label: '创建人', width: '', align: 'center', showTooltip: true},
      ],
      // list
      listData: [],
      tableLoading: false,
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
      state.tableLoading = true
      useUserApi().getList(state.listQuery)
          .then(res => {
            state.listData = res.data.rows
            state.total = res.data.rowTotal
            state.tableLoading = false
          })
    };

    const getRolesList = () => {
      useRolesApi().getList(state.roleQuery)
          .then((res: any) => {
            state.roleList = res.data.rows
          })
    };

    // 查询
    const search = () => {
      state.listQuery.page = 1
      getList()
    }

    // 新增或修改用户
    const onOpenSaveOrUpdate = (editType: string, row?: TableDataRow) => {
      saveOrUpdateRef.value.openDialog(editType, row);
    };

    // 删除用户
    const deleted = (row: TableDataRow) => {
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
    const handleRoles = (roles: any) => {
      let roleTagList: any[] = []
      roles.forEach((role: any) => {
        let roleName = state.roleList.find(e => e.id == role)?.name
        roleTagList.push(h(ElTag, null, roleName))
      })
      return h('div', null, roleTagList)
    }
    // 页面加载时
    onMounted(() => {
      getList();
      getRolesList()
    });
    return {
      getList,
      search,
      saveOrUpdateRef,
      onOpenSaveOrUpdate,
      deleted,
      store,
      userInfos,
      getRolesList,
      handleRoles,
      ...toRefs(state),
    };
  },
});
</script>
