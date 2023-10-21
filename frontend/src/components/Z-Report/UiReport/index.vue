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
              placeholder="名称查询"
              style="width: 200px;"
              class="ml10"
              @keyup.enter.native="searchDetail"/>

          <el-button class="ml10" type="primary" @click="searchDetail">
            查询
          </el-button>
        </div>

        <!--       tool      -->
        <div class="mb8 mt8">
          <el-checkbox class="ml10" v-model="state.viewErrOrFailApiStatus" @change="viewErrOrFailApi">
            只看错误/失败步骤
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
              :showPage="false"
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

</template>

<script setup name="UiReportDetail">
import {h, nextTick, reactive} from "vue";
import {ElButton, ElImage} from "element-plus";
import {useRouter} from "vue-router"
import {useUiReportApi} from "/@/api/useUiApi/uiReport";
import {getStatusTag} from "/@/utils/case"
import ReportStatistics from "./uiReportStatistics.vue"
import {useUserInfo} from '/@/stores/userInfo';
import {storeToRefs} from "pinia";
import {getBaseApiUrl} from "/@/utils/config"

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
    {label: 'N', columnType: 'index', align: '', width: 'auto', showTooltip: false},
    {
      key: 'name', label: '名称', align: '', width: 'auto', show: true,
      render: ({row}) => h(ElButton, {
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
      key: 'duration',
      label: '执行耗时(s)',
      align: '',
      width: '',
      show: true,
    },
    {
      key: 'action',
      label: '动作',
      align: '',
      width: '',
      show: true,
    },
    {
      key: '', label: '元素', align: "", width: 'auto', show: true,
      render: ({row}) => h('div', null, [
        h('div', {}, `定位方法: ${row.location_method}`),
        h('div', {}, `定位值: ${row.location_value}`),
      ])
    },
    {
      key: 'data',
      label: "数据",
      align: '',
      width: '',
      show: true,
    },
    {key: 'message', label: '错误信息', align: "", width: 'auto', show: true},
    {
      key: 'screenshot',
      label: "截图",
      align: '',
      width: '',
      show: true,
      render: ({row}) => h(ElImage, {
        src: `${getBaseApiUrl()}/${row.screenshot_url}`,
        fit: "contain",
        previewSrcList: state.screenshotUrlList,
        previewTeleported: true,
        style: {
          width: "60px",
          height: "50px",
        }
      })
    },
    {
      label: '操作', columnType: 'string', fixed: 'right', align: '', width: '200',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: getStatusTag(row.status),
          plain: true,
        }, () => row.status ? row.status.toUpperCase() : "-"),
        h(ElButton, {
          type: "primary",
          title: "查看日志",
          onClick: () => {
            viewDetail(row)
          }
        }, () => '日志')
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
    report_id: null,
    name: null,
    api_name: null,
    url: null,
    step_type: "",
    parent_step_id: null,
    status_list: []
  },
  tableLoading: false,
  listData: [],
  // show showDetailInfo
  showDetailInfo: false,
  reportData: {},
  // statisticsData
  statisticsData: {},
  statQuery: {
    report_id: null,
  },

//   screenshot
  screenshotUrlList: [],

})

const initReport = () => {
  state.start_time = props.reportInfo.start_time
  state.exec_user_name = userInfos.value.nickname

  state.listQuery.report_id = state.statQuery.report_id = state.report_id = props.reportInfo.id
  state.start_time = props.reportInfo.start_time
  state.exec_user_name = props.reportInfo.exec_user_name
  if (state.report_id) {
    getDetails()
    getStatistics()
  }
}
// 获取报告列表
const getDetails = () => {
  state.tableLoading = true
  useUiReportApi().getReportDetail(state.listQuery).then((res) => {
    state.listData = res.data
    if (res.data.length > 0) {
      state.screenshotUrlList = res.data.map((item) => {
        return `${config.url}/${item.screenshot_url}`
      })
    }
    state.tableLoading = false
  }).catch(() => {
    state.tableLoading = false
  })
}

// 查询重置页数
const searchDetail = () => {
  getDetails()
}

// 查看错误或者失败的api
const viewErrOrFailApi = (value) => {
  state.listQuery.status_list = []
  if (value) {
    state.listQuery.status_list = ["ERROR", "FAILURE"]
  }
  getDetails()
}

// 获取统计数据
const getStatistics = () => {
  useUiReportApi().getReportStatistics(state.statQuery).then((res) => {
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
  let res = await useUiReportApi().getReportDetail(state.listQuery)
  resolve(res.data.rows)
}

const showReport = () => {
  state.showReportDialog = !state.showReportDialog
  nextTick(() => {
    initReport()
  })
}

const toApiInfo = (row) => {
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