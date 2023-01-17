<template>
  <el-dialog
      draggable
      v-if="state.showReportDialog"
      v-model="state.showReportDialog"
      width="80%"
      top="5vh"
      destroy-on-close
      :close-on-click-modal="false">
    <template #header>
      <span>报告详情</span>
      <el-button class="ml5" style="font-size: 12px" type="primary" link @click="state.showLog=!state.showLog">
        执行日志
      </el-button>
    </template>

    <div class="">
      <el-card style="margin-bottom: 10px">
        <ReportStatistics :data="state.statisticsData"
                          :run_user_name="state.run_user_name"
                          :start_time="state.start_time">
        </ReportStatistics>
      </el-card>
      <el-card>
        <z-table
            :columns="state.columns"
            :data="state.listData"
            row-key="id"
            :lazy="true"
            :load="getChildrenData"
            v-model:page-size="state.listQuery.pageSize"
            v-model:page="state.listQuery.page"
            :total="state.total"
            :tree-props="{ children: 'children', hasChildren: 'has_step_data' }"
            @pagination-change="getList"
        ></z-table>
      </el-card>

      <div>
        <el-drawer
            v-model="state.showDetailInfo"
            size="70%"
            append-to-body
            direction="ltr"
            title="报告详情"
            :with-header="true">
          <z-api-report :reportData="state.reportData"/>
        </el-drawer>
      </div>

    </div>
  </el-dialog>

  <el-dialog
      draggable
      v-if="state.showReportDialog"
      v-model="state.showLog"
      width="80%"
      top="8vh"
      destroy-on-close
      :close-on-click-modal="false">
    <template #header>
      <span>日志</span>
    </template>
    <pre>{{ reportInfo.run_log }}</pre>
  </el-dialog>
</template>

<script lang="ts" setup name="ReportDetail">
import {h, onMounted, reactive, watch} from "vue";
import {ElButton, ElTag} from "element-plus";
import {useReportApi} from "/@/api/useAutoApi/report";
import {getMethodColor, getStatusTag} from "/@/utils/case"
import ReportStatistics from "./ReportStatistics.vue"

const props = defineProps({
  reportInfo: {
    type: Object,
  }
})

const state = reactive({
  columns: [
    {label: 'N', columnType: 'index', align: 'center', width: 'auto', showTooltip: false},
    {
      key: 'name', label: '名称', align: 'center', width: 'auto', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          if (row.step_type === 'case' && row.status !== 'SKIP') {
            viewDetail(row)
          }
        }
      }, () => row.name)
    },
    {
      key: 'method', label: '请求方法', align: 'center', width: '', show: true,
      render: (row: any) => row.method ? h(ElTag, {
        type: "",
        style: {"background": getMethodColor(row.method), color: "#ffffff",}
      }, () => row.method) : ""
    },
    {key: 'url', label: 'url', align: 'center', width: '', show: true},
    {
      key: 'step_type', label: '步骤类型', align: 'center', width: '', show: true,
      lookupCode: "api_step_type"
    },
    {
      key: 'case_name',
      label: '接口名称',
      width: '',
      align: 'center',
      show: true,
      lookupCode: 'api_report_run_type'
    },
    {
      key: 'status_code', label: 'HttpCode', width: '', align: 'center', show: true,
      render: (row: any) => row.status_code ? h(ElTag, {
        type: row.status_code == 200 ? "success" : "warning",
      }, () => row.status_code == 200 ? "200 OK" : row.status_code) : ""
    },
    {
      key: 'run_mode',
      label: '运行模式',
      align: 'center',
      width: '',
      show: true,
      lookupCode: 'api_report_run_mode'
    },
    // {key: 'has_step_data', label: '子步骤', align: 'center', width: '', show: true},
    {key: 'case_name', label: '用例名', align: 'center', width: '', show: true},
    {key: 'run_count', label: '运行数', align: 'center', width: '', show: true},
    {
      key: 'status', label: 'Status', align: "center", width: 'auto', show: true,
      render: (row: any) => h(ElTag, {
        type: getStatusTag(row.status),
      }, () => row.status.toUpperCase())
    },
    {key: 'message', label: '错误信息', align: "center", width: 'auto', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: 'auto',
      render: (row: any) => h("div", null, [
        h(ElButton, {
          link: true,
          type: "primary",
          disabled: row.step_type !== 'case' || row.status === 'SKIP',
          onClick: () => {
            if (row.step_type === 'case' && row.status !== 'SKIP') {
              viewDetail(row)
            }
          }
        }, () => '查看')
      ])
    },
  ],
  // show report:
  showReportDialog: false,
  showLog: false,
  // report_info
  report_id: null,
  start_time: null,
  run_user_name: null,

  listQuery: {
    page: 1,
    pageSize: 20,
    id: null,
    name: null,
    min_and_max: null,
    execute_user_name: null,
    responsible_name: null,
    status: null,
    ids: [],
  },
  listData: [],
  total: 0,

  // show showDetailInfo
  showDetailInfo: false,
  reportData: {},
  // statisticsData
  statisticsData: {},
  statQuery: {
    id: null,
  },
})

const initReport = () => {
  state.report_id = props.reportInfo.id
  state.start_time = props.reportInfo.start_time
  state.run_user_name = props.reportInfo.run_user_name
  state.listQuery.id = state.report_id
  state.statQuery.id = state.report_id
  if (state.report_id) {
    getList()
    getStatistics()
  }
}

// 获取报告列表
const getList = () => {
  useReportApi().getReportDetail(state.listQuery).then((res: any) => {
    state.listData = res.data.rows
    state.total = res.data.rowTotal
  })
}

// 获取统计数据
const getStatistics = () => {
  useReportApi().getReportStatistics(state.statQuery).then((res: any) => {
    state.statisticsData = res.data
  })
}

// 查看详情
const viewDetail = (row: any) => {
  state.reportData = row
  state.showDetailInfo = true
}

// 获取子步骤数据
const getChildrenData = async (row: any, treeNode: any, resolve: any) => {
  state.listQuery.id = 3
  state.listQuery.parent_step_id = row.step_id
  let res = await useReportApi().getReportDetail(state.listQuery)
  resolve(res.data.rows)
}

const showReport = () => {
  state.showReportDialog = !state.showReportDialog
}

onMounted(() => {
  initReport()
})

watch(
    () => props.reportInfo,
    (val) => {
      if (val) {
        initReport()
      }
    },
    {
      deep: true,
      // immediate: true,
    }
);

defineExpose({
  showReport,
})


</script>

<style lang="scss" scoped>

</style>