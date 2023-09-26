<template>
  <el-dialog
      draggable
      v-if="state.showReportDialog"
      v-model="state.showReportDialog"
      width="90%"
      top="5vh"
      destroy-on-close
      :close-on-click-modal="false">
    <template #header>
      <strong>报告详情</strong>
      <!--      <el-button class="ml5" style="font-size: 12px" type="primary" link @click="state.showLog=!state.showLog">-->
      <!--        执行日志-->
      <!--      </el-button>-->
    </template>

    <div class="">
      <el-card style="margin-bottom: 10px">
        <ReportStatistics :data="state.statisticsData"
                          :exec_user_name="state.exec_user_name"
                          :start_time="state.start_time">
        </ReportStatistics>
      </el-card>
      <el-card>
        <!--        search      -->
        <div v-show="!isDebug">
          <el-input
              clearable
              v-model="state.listQuery.name"
              placeholder="用例名称"
              style="width: 200px;"
              class="ml10"
              @keyup.enter.native="searchDetail"/>
          <el-input
              clearable
              v-model="state.listQuery.api_name"
              placeholder="接口名称" style="width: 150px;"
              class="ml10"
              @keyup.enter.native="searchDetail"/>
          <el-input
              clearable
              v-model="state.listQuery.url"
              placeholder="url查询" style="width: 150px;"
              class="ml10"
              @keyup.enter.native="searchDetail"/>

          <el-button class="ml10" type="primary" @click="searchDetail">
            查询
          </el-button>


        </div>

        <!--       tool      -->
        <div class="mb8 mt8">
          <el-checkbox class="ml10" v-model="state.viewErrOrFailApiStatus" @change="viewErrOrFailApi">
            只看错误/失败接口
          </el-checkbox>
        </div>

        <!--        search      -->
        <div>
          <z-table
              :columns="state.columns"
              :data="state.listData"
              row-key="id"
              :lazy="true"
              :showPlaceholder="true"
              :loading="state.tableLoading"
              :load="getChildrenData"
              v-model:page-size="state.listQuery.pageSize"
              v-model:page="state.listQuery.page"
              :total="state.total"
              :tree-props="{ children: 'children', hasChildren: 'has_step_data' }"
              @pagination-change="getList"
          ></z-table>
        </div>
      </el-card>

      <div>
        <el-drawer
            v-model="state.showDetailInfo"
            size="70%"
            append-to-body
            direction="ltr"
            destroy-on-close
            :with-header="true">
          <template #header>
            <strong>报告详情</strong>
          </template>
          <z-api-report :reportData="state.reportData"/>
        </el-drawer>
      </div>

    </div>
  </el-dialog>

  <!--  <el-dialog-->
  <!--      draggable-->
  <!--      v-if="state.showReportDialog"-->
  <!--      v-model="state.showLog"-->
  <!--      width="80%"-->
  <!--      top="8vh"-->
  <!--      destroy-on-close-->
  <!--      :close-on-click-modal="false">-->
  <!--    <template #header>-->
  <!--      <span>日志</span>-->
  <!--    </template>-->
  <!--    <pre>{{ reportInfo.run_log }}</pre>-->
  <!--  </el-dialog>-->
</template>

<script lang="ts" setup name="ReportDetail">
import {h, reactive, nextTick} from "vue";
import {ElButton, ElTag} from "element-plus";
import {useRouter} from "vue-router"
import {useReportApi} from "/@/api/useAutoApi/report";
import {getMethodColor, getStatusTag} from "/@/utils/case"
import ReportStatistics from "./ReportStatistics.vue"
import {Promotion} from "@element-plus/icons"
import {useUserInfo} from '/@/stores/userInfo';
import {storeToRefs} from "pinia";

const stores = useUserInfo();
const {userInfos} = storeToRefs(stores);

const props = defineProps({
  reportInfo: {
    type: Object,
    default: () => {
      return {}
    }
  },
  isDebug: {
    type: Boolean,
    default: () => {
      return false
    }
  },
})

const router = useRouter()

const state = reactive({
  columns: [
    {label: 'N', columnType: 'index', align: 'center', width: 'auto', showTooltip: false},
    {
      key: 'name', label: '名称', align: 'center', width: 'auto', show: true,
      render: ({row}: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          if (row.status !== 'SKIP') {
            viewDetail(row)
          }
        }
      }, () => row.name)
    },
    {
      key: 'method', label: '请求方法', align: 'center', width: '', show: true,
      render: ({row}: any) => row.method ? h(ElTag, {
        type: "",
        style: {"background": getMethodColor(row.method), color: "#ffffff",}
      }, () => row.method) : "-"
    },
    {key: 'url', label: 'url', align: 'center', width: '', show: true},
    {
      key: 'step_type', label: '步骤类型', align: 'center', width: '', show: true,
      lookupCode: "api_step_type"
    },
    {
      key: 'step_tag', label: '步骤标签', align: 'center', width: '', show: true,
      render: ({row}: any) => row.step_tag ? h(ElTag, {
        type: getStatusTag(row.status),
      }, () => row.step_tag) : "-"
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
      render: ({row}: any) => row.status_code ? h(ElTag, {
        type: row.status_code == 200 ? "success" : "warning",
      }, () => row.status_code == 200 ? "200 OK" : row.status_code) : "-"
    },
    {
      key: 'elapsed_ms',
      label: '请求耗时(ms)',
      align: 'center',
      width: '',
      show: true,
    },
    {
      key: 'duration',
      label: '执行耗时(s)',
      align: 'center',
      width: '',
      show: true,
    },
    // {key: 'has_step_data', label: '子步骤', align: 'center', width: '', show: true},
    {key: 'case_name', label: '用例名', align: 'center', width: '', show: true},
    // {key: 'run_count', label: '运行数', align: 'center', width: '', show: true},
    {
      key: 'status', label: '状态', align: "center", width: 'auto', show: true,
      render: ({row}: any) => h(ElTag, {
        type: getStatusTag(row.status),
      }, () => row.status? row.status.toUpperCase() : "-")
    },
    {key: 'message', label: '错误信息', align: "center", width: 'auto', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '150',
      render: ({row}: any) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            if (row.status !== 'SKIP') {
              viewDetail(row)
            }
          }
        }, () => '查看'),
        h(ElButton, {
          type: "warning",
          disabled: row.step_type !== 'api',
          title: "跳转到api",
          icon: Promotion,
          onClick: () => {
            if (row.status !== 'SKIP') {
              toApiInfo(row)
            }
          }
        }, () => '跳转')
      ])
    },
  ],
  // show report:
  showReportDialog: false,
  showLog: false,
  // report_info
  report_id: null,
  start_time: "",
  exec_user_name: "",
  // view
  viewErrOrFailApiStatus: false,

  listQuery: {
    page: 1,
    pageSize: 20,
    id: null,
    name: null,
    api_name: null,
    url: null,
    step_type: "",
    parent_step_id: null,
    status_list: []
  },
  tableLoading: false,
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
  state.start_time = props.reportInfo.start_time
  state.exec_user_name = userInfos.value.nickname
  if (props.isDebug) {
    state.listData = props.reportInfo.step_results
    state.statisticsData = getStatisticsDataByDebug(props.reportInfo.step_results)
  } else {
    state.report_id = props.reportInfo.id
    state.start_time = props.reportInfo.start_time
    state.exec_user_name = props.reportInfo.exec_user_name
    state.listQuery.id = state.report_id
    state.statQuery.id = state.report_id
    if (state.report_id) {
      getList()
      getStatistics()
    }
  }
}

const getStatisticsDataByDebug = (step_results: Array<StepResult>) => {
  let reportInfo = props.reportInfo
  let statisticsData = {
    actual_run_count: reportInfo.actual_run_count,
    count_step: step_results.length,
    count_step_success: reportInfo.run_success_count,
    count_step_failure: reportInfo.run_fail_count,
    count_step_skip: reportInfo.run_skip_count,
    count_step_error: reportInfo.run_err_count,
    avg_request_time: 0,
    count_request_time: 0,
    count_case: 0,
    count_case_success: 0,
    count_case_fail: 0,
    case_pass_rate: 0,
    step_pass_rate: 0
  }
  let elapsed_ms: number = 0
  statisticsData.step_pass_rate = Math.round((statisticsData.count_step_success / statisticsData.actual_run_count) * 100)

  step_results.forEach((e: any) => {
    if (e.step_type == 'api') {
      e.url = e.session_data.req_resp.request.url
      e.method = e.session_data.req_resp.request.method
      e.status_code = e.session_data.req_resp.response.status_code
      e.elapsed_ms = e.session_data.stat.elapsed_ms
      elapsed_ms += e.session_data.stat.elapsed_ms
      statisticsData.count_request_time += e.duration
      statisticsData.count_case++
      if (e.status == "SUCCESS") {
        statisticsData.count_case_success += 1
      } else {
        statisticsData.count_case_fail += 1
      }
    }
  })
  statisticsData.count_request_time = Math.round(statisticsData.count_request_time * 100) / 100
  statisticsData.avg_request_time = Math.round((elapsed_ms / statisticsData.count_case) * 100) / 100
  statisticsData.case_pass_rate = Math.round((statisticsData.count_case_success / statisticsData.count_case) * 100)

  return statisticsData
}

// 获取报告列表
const getList = () => {
  state.tableLoading = true
  useReportApi().getReportDetail(state.listQuery).then((res: any) => {
    state.listData = res.data.rows
    state.total = res.data.rowTotal
    state.tableLoading = false
  }).catch(() => {
    state.tableLoading = false
  })
}

// 查询重置页数
const searchDetail = () => {
  state.listQuery.page = 1
  getList()
}

// 查看错误或者失败的api
const viewErrOrFailApi = (value: any) => {
  state.listQuery.step_type = ""
  state.listQuery.status_list = []
  if (value) {
    state.listQuery.step_type = "api"
    state.listQuery.status_list = ["ERROR", "FAILURE"]
  }
  getList()
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
  state.listQuery.id = row.id
  state.listQuery.parent_step_id = row.step_id
  let res = await useReportApi().getReportDetail(state.listQuery)
  resolve(res.data.rows)
}

const showReport = () => {
  state.showReportDialog = !state.showReportDialog
  nextTick(() => {
    initReport()
  })
}

const toApiInfo = (row: any) => {
  router.push({name: "EditApiInfo", query: {editType: "update", id: row.case_id}})
}

// watch(
//     () => props.reportInfo,
//     (val) => {
//       if (val) {
//         initReport()
//       }
//     },
//     {
//       deep: true,
//       // immediate: true,
//     }
// );

defineExpose({
  showReport,
})


</script>

<style lang="scss" scoped>

</style>