<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入名称" style="max-width: 180px"></el-input>
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
      >
      </z-table>
    </el-card>
  </div>
</template>

<script setup name="uiPage">
import {ElButton, ElMessage, ElMessageBox} from "element-plus";
import {h, onMounted, reactive, ref} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import {useRouter} from 'vue-router'

const tableRef = ref();
const router = useRouter();

const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {
      key: 'name', label: '页面名称', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'url', label: 'url', width: '', align: 'center', show: true},
    {key: 'element_count', label: '元素数量', width: '', align: 'center', show: true},
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {key: 'module_name', label: '所属模块', width: '', align: 'center', show: true},
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
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
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
});

const search = () => {
  state.listQuery.page = 1
  getList()
};

const getList = () => {
  tableRef.value.openLoading()
  useUiPageApi().getList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows;
      state.total = res.data.rowTotal;

    })
    .finally(() => {
      tableRef.value.closeLoading()
    })
};

// 新增或修改
const onOpenSaveOrUpdate = (editType, row) => {
  let query = {}
  query.editType = editType
  if (row) query.id = row.id
  router.push({name: 'EditPage', query: query})
};


// 删除
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      useUiPageApi().deleted({id: row.id})
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

<style scoped lang="scss">

</style>