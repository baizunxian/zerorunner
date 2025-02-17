<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入配置名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增</el-button>
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

    <el-dialog
        draggable
        v-model="state.showSaveOrUpdate"
        width="50%"
        top="8vh"
        :title="state.editType === 'save'? '新增配置':'更新配置'"
        destroy-on-close
        :close-on-click-modal="false">
      <EditEnv ref="EditEnvRef" @getList="getList" :env_id="state.env_id"/>
      <template #footer>
        <el-button @click="state.showSaveOrUpdate = false">取 消</el-button>
        <el-button type="primary" @click="saveOrUpdate">保 存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ApiEnv">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useEnvApi} from "/@/api/useAutoApi/env";
import EditEnv from './components/EditEnv.vue';

const EditEnvRef = ref();
const tableRef = ref();
const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', width: 'auto', align: 'center', show: true},
    {
      key: 'name', label: '环境名称', width: '', align: 'center', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'domain_name', label: '域名地址', width: 'auto', align: 'center', show: true},
    {key: 'remarks', label: '备注', width: 'auto', align: 'center', show: true},
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
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    case_type: 2,
    name: '',
  },
  // configure
  editType: 'save',
  env_id: null,
  showSaveOrUpdate: false,
});
// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useEnvApi().getList(state.listQuery)
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
  state.editType = editType
  if (row && row.id) {
    state.env_id = row.id
  } else {
    state.env_id = null
  }
  state.showSaveOrUpdate = !state.showSaveOrUpdate
  // router.push({name: 'saveOrUpdateTestCase', query: query})
};

// saveOrUpdate
const saveOrUpdate = () => {
  EditEnvRef.value.saveOrUpdate()
};

// 删除角色
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useEnvApi().deleted({id: row.id})
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
