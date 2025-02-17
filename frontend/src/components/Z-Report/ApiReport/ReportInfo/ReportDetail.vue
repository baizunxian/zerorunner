<template>
  <div class="app-container">
    <el-card style="margin-bottom: 10px">
      <div class="report-seal"
           v-show="JSON.stringify(state.statisticsData) !== '{}'"
           :style="{border: `solid 4px var(${reportStatus? '--el-color-success': '--el-color-danger'})`}">
        <div class="report-seal-son"
             :style="{border: `solid 2px var(${reportStatus? '--el-color-success': '--el-color-danger'})`,
           color: `var(${reportStatus? '--el-color-success': '--el-color-danger'})`
      }">
          <span class="report-seal-text">{{ reportStatus ? "通过" : "不通过" }}</span>
        </div>
      </div>
      <ReportStatistics :data="state.statisticsData"></ReportStatistics>
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
        <el-checkbox class="ml10" v-show="!props.isDebug" v-model="state.viewErrOrFailApiStatus"
                     @change="viewErrOrFailApi">
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
            :show-page="!isDebug"
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
            <span>
              <strong class="pr10">报告详情</strong>
               <el-tag type="danger" v-if="state.reportData?.success === 0">不通过</el-tag>
               <el-tag type="success" v-else>通过</el-tag>
            </span>

        </template>
        <z-api-report :reportData="state.reportData"/>
      </el-drawer>
    </div>

  </div>
</template>

<script setup name="ReportDetail">
import {h, reactive, nextTick, watch, onMounted, computed} from "vue";
import {ElButton, ElTag} from "element-plus";
import {useRouter, useRoute} from "vue-router"
import {useReportApi} from "/@/api/useAutoApi/report";
import {getMethodColor, getStatusTag} from "/@/utils/case"
import ReportStatistics from "../components/ReportStatistics.vue"
import {Promotion} from "@element-plus/icons"
import {useUserInfo} from '/@/stores/userInfo';
import {storeToRefs} from "pinia";

const stores = useUserInfo();
const {userInfos} = storeToRefs(stores);

const props = defineProps({
  reportId: {
    type: Number || String,
    default: () => {
      return null
    }
  },
  reportInfo: {
    type: Object,
    default: () => {
      return {}
    }
  },
  isDebug: {
    type: Boolean,
    default: () => {
      return null
    }
  },
})

const router = useRouter()
const route = useRoute()

const state = reactive({
  columns: [
    {label: 'N', columnType: 'index', align: 'center', width: 'auto', showTooltip: false},
    {
      key: 'name', label: '名称', align: 'center', width: 'auto', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          viewDetail(row)
        }
      }, () => row.name)
    },
    {
      key: 'method', label: '请求方法', align: 'center', width: '', show: true,
      render: ({row}) => row.method ? h(ElTag, {
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
      render: ({row}) => row.step_tag ? h(ElTag, {
        type: getStatusTag(row.status),
      }, () => row.step_tag) : "-"
    },
    {
      key: 'name',
      label: '接口名称',
      width: '',
      align: 'center',
      show: true,
    },
    {
      key: 'status_code', label: 'HttpCode', width: '', align: 'center', show: true,
      render: ({row}) => row.status_code ? h(ElTag, {
        type: row.status_code === 200 ? "success" : "warning",
      }, () => row.status_code === 200 ? "200 OK" : row.status_code) : "-"
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
      render: ({row}) => h(ElTag, {
        type: getStatusTag(row.status),
      }, () => row.status ? row.status.toUpperCase() : "-")
    },
    {key: 'message', label: '错误信息', align: "center", width: 'auto', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '150',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            viewDetail(row)
          }
        }, () => '查看'),
        h(ElButton, {
          type: "warning",
          disabled: row.step_type !== 'api',
          title: "跳转到api",
          icon: Promotion,
          onClick: () => {
            toApiInfo(row)
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
  const isDebug = props.isDebug || route.query.isDebug
  const report_id = props.reportId || route.query.id
  state.start_time = props.reportInfo.start_time
  state.exec_user_name = userInfos.value.nickname
  if (isDebug) {
    state.listData = props.reportInfo.step_results
    state.statisticsData = getStatisticsDataByDebug(props.reportInfo.step_results)
  } else {
    state.report_id = state.listQuery.id = state.statQuery.id = report_id
    if (report_id) {
      getList()
      getStatistics()
    }
  }
}

const getStatisticsDataByDebug = (step_results) => {
  let reportInfo = props.reportInfo
  let statisticsData = {
    actual_run_count: reportInfo.actual_run_count,
    step_count: step_results.length,
    step_success_count: reportInfo.run_success_count,
    step_fail_count: reportInfo.run_fail_count,
    step_skip_count: reportInfo.run_skip_count,
    step_error_count: reportInfo.run_err_count,
    avg_request_time: 0,
    count_request_time: 0,
    case_count: 0,
    case_success_count: 0,
    case_fail_count: 0,
    case_pass_rate: 0,
    step_pass_rate: 0,
    start_time: reportInfo.start_time,
    exec_user_name: userInfos.value.nickname,
    success: reportInfo.success
  }
  let elapsed_ms = 0
  statisticsData.step_pass_rate = Math.round((statisticsData.step_success_count / statisticsData.actual_run_count) * 100)

  step_results.forEach((e) => {
    if (e.step_type === 'api') {
      e.url = e.session_data.req_resp.request.url
      e.method = e.session_data.req_resp.request.method
      e.status_code = e.session_data.req_resp.response.status_code
      e.elapsed_ms = e.session_data.stat.elapsed_ms
      elapsed_ms += e.session_data.stat.elapsed_ms
      statisticsData.request_time_count += e.duration
      statisticsData.case_count++
      if (e.status === "SUCCESS") {
        statisticsData.case_success_count += 1
      } else {
        statisticsData.case_fail_count += 1
      }
    }
  })
  statisticsData.request_time_count = Math.round(statisticsData.request_time_count * 100) / 100
  statisticsData.avg_request_time = Math.round((elapsed_ms / statisticsData.case_count) * 100) / 100
  statisticsData.case_pass_rate = Math.round((statisticsData.case_success_count / statisticsData.case_count) * 100)

  return statisticsData
}

// 获取报告列表
const getList = () => {
  state.tableLoading = true
  useReportApi().getReportDetail(state.listQuery).then((res) => {
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
const viewErrOrFailApi = (value) => {
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
  useReportApi().getReportStatistics(state.statQuery).then((res) => {
    state.statisticsData = res.data
  })
}

// 查看详情
const viewDetail = (row) => {
  state.reportData = row
  state.showDetailInfo = true
}

// 获取子步骤数据
const getChildrenData = async (row, treeNode, resolve) => {
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

const toApiInfo = (row) => {
  router.push({name: "EditApiInfo", query: {editType: "update", id: row.source_id}})
}

// 获取报告状态，通过，不通过
const reportStatus = computed(() => {
  return state.statisticsData?.success === 1 || state.statisticsData?.success
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

watch(
    () => props.report_id,
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

onMounted(() => {
  initReport()
})

defineExpose({
  showReport,
})


</script>

<style lang="scss" scoped>

.report-seal {
  z-index: 1;
  position: absolute;
  right: 10px;
  margin-top: -30px;
  //top: 5px;
  width: 80px;
  height: 80px;
  //border: solid 4px var(--el-color-success);
  border-radius: 100%;
  background-color: var(--el-tag--success-color);
  display: flex;
  justify-content: center;
  align-items: center;
}

.report-seal-son {
  width: 60px;
  height: 60px;
  line-height: 60px;
  //border: solid 2px var(--el-color-success);
  border-radius: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  position: relative;
  text-align: center;
  vertical-align: middle;
  transform: rotate(45deg);
  //color: var(--el-color-success);
  font-size: 16px;
  font-weight: 900;
}

</style>