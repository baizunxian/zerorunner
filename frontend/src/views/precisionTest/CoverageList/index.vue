<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="state.listQuery.name" placeholder="输入报告名查询" style="max-width: 180px"></el-input>
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
  </div>
</template>

<script setup name="CoverageList">
import {h, onMounted, reactive, ref} from 'vue';
import {useRouter} from "vue-router";
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import {useCoverageReportApi} from "/@/api/useCoverageApi/coverage";

const router = useRouter()
// 自定义数据
const tableRef = ref();
const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
    {
      key: 'name', label: '项目名称', align: 'center', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenReportDetail(row)
        }
      }, () => row.name)
    },
    {
      key: 'coverage_type', label: '覆盖类型', align: 'center', width: '', show: true,
      render: ({row}) => h(ElTag, {
        type: row.coverage_type === 10 ? "warning" : "success",
      }, () => row.coverage_type === 10 ? "全量" : "增量")
    },
    {key: 'coverage_rate', label: '覆盖率', align: 'center', width: '', show: true},
    {key: 'new_branches', label: '比对分支', align: 'center', width: '', show: true},
    {key: 'new_last_commit_id', label: 'newCommitId', align: 'center', width: '', show: true},
    {key: 'old_branches', label: '基准分支', align: 'center', width: '', show: true},
    {key: 'old_last_commit_id', label: 'oldCommitId', align: 'center', width: '', show: true},


    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenReportDetail(row)
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
  useCoverageReportApi().getList(state.listQuery)
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
const onOpenReportDetail = (row) => {
  router.push({path: '/precisionTest/CoverageDetail', query: {id: row.id}})
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
