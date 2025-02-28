<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            clearable
            v-model="state.listQuery.name"
            placeholder="输入报告名查询"
            style="width: 200px;"
            class=""
            @keyup.enter.native="search"/>
        <el-input
            clearable
            v-model="state.listQuery.exec_user_name"
            placeholder="输入执行人查询" style="width: 150px;"
            class="ml10"
            @keyup.enter.native="search"/>

        <el-button class="ml10" type="primary" @click="search">
          查询
        </el-button>

      </div>

      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          v-model:total="state.total"
          @pagination-change="getList"
      />

<!--      <ReportDetail :report-info="state.reportInfo"/>-->

    </el-card>
  </div>
</template>

<script setup name="apiReport">
import {useReportApi} from '/@/api/useAutoApi/report';
import {useRouter} from "vue-router";
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus'
import ReportDetail from "/@/components/Z-Report/ApiReport/ReportInfo/ReportDetail.vue"

const tableRef = ref()
const router = useRouter()
const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
    {
      key: 'name', label: '报告名称', align: 'center', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenReport(row)
        }
      }, () => row.name)
    },
    {
      key: 'status', label: '运行结果', align: 'center', width: '', show: true,
      render: ({row}) => h(ElTag, {
        type: row.success ? "success" : "danger",
      }, () => row.success ? "通过" : "不通过",)
    },
    {
      key: 'run_type',
      label: '任务类型',
      width: '',
      align: 'center',
      showTooltip: true,
      lookupCode: 'api_report_run_type'
    },
    {
      key: 'run_mode',
      label: '运行模式',
      align: 'center',
      width: '',
      showTooltip: true,
      lookupCode: 'api_report_run_mode'
    },
    {key: 'run_count', label: '运行数', align: 'center', width: '', show: true},
    // {key: 'successes', label: '执行结果', width: '', showTooltip: true},
    {key: 'run_success_count', label: '成功数', align: 'center', width: '', show: true},
    {key: 'duration', label: '运行耗时(秒)', align: 'center', width: '', show: true},
    {key: 'start_time', label: '运行时间', align: 'center', width: '150', show: true},
    {key: 'exec_user_name', label: '执行人', align: 'center', width: '', show: true},
    {key: 'error_msg', label: '错误信息', align: 'center', width: '', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '140',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenReport(row)
          }
        }, () => '查看'),
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
  showReportDialog: false,
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    id: null,
    name: null,
    min_and_max: null,
    exec_user_name: null,
    status: null,
    ids: [],
    case_id: null,
    api_id: null
  },
  // report
  reportInfo: {},
});

// 获取列表
const getList = () => {
  tableRef.value.openLoading()
  useReportApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      });
};

// 查询
const search = () => {
  state.listQuery.page = 1
  getList()
}

// 删除报告
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    useReportApi().deleted({'id': row.id}).then(() => {
      ElMessage.success('删除成功！')
      getList()
    })
  })
}

const onOpenReport = (row) => {
  state.reportInfo = row
  router.push({name: 'ApiReportDetail', query: {id: row.id}})
  // reportDetailRef.value.showReport()
}

// watch(
//     () => route.query,
//     (query: any) => {
//       state.listQuery.case_id = query.case_id ? query.case_id : null
//       state.listQuery.api_id = query.api_id ? query.api_id : null
//       getList()
//     },
//     {deep: true}
// )

// 获取列表
onMounted(() => {
  getList()
})

</script>

<style lang="scss" scoped>
</style>
