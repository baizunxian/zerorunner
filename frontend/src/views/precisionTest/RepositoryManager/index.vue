<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="输入仓库查询" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
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

    <CoverageInfo ref="CoverageInfoRef"></CoverageInfo>
  </div>
</template>

<script setup name="RepositoryManager">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useRepositoryApi} from "/@/api/useCoverageApi/repository";
import CoverageInfo from "/@/views/precisionTest/RepositoryManager/coverageInfo.vue";
import {useCoverageReportApi} from "/@/api/useCoverageApi/coverage";

// 自定义数据
const tableRef = ref();
const CoverageInfoRef = ref();
const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
    {
      key: 'name', label: '仓库名称', align: 'center', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        // onClick: () => {
        //   onOpenReportDetail(row)
        // }
      }, () => row.name)
    },
    {key: 'html_url', label: '仓库地址', align: 'center', width: '', show: true},

    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenCoveragePage(row)
          }
        }, () => '覆盖率'),

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
  useRepositoryApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data
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
const onOpenCoveragePage = (row) => {
  CoverageInfoRef.value.openDialog(row)
};

// 删除角色
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useCoverageReportApi().deleted({id: row.id})
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
