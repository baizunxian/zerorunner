<template>
  <div class="">
    <el-card style="margin-bottom: 10px">
      <echarts-statistics :data="statisticsData"
                          :run_user_name="run_user_name"
                          :start_time="start_time">
      </echarts-statistics>
    </el-card>
    <el-card>
      <zero-table
          :columns="columns"
          :data="listData"
          row-key="id"
          :lazy="true"
          :load="getChildrenData"
          v-model:page-size="listQuery.pageSize"
          v-model:page="listQuery.page"
          :total="total"
          :tree-props="{ children: 'children', hasChildren: 'has_step_data' }"
          @pagination-change="getList"
      ></zero-table>
    </el-card>

    <div>
      <el-drawer
          v-model="showDetailInfo"
          size="70%"
          direction="ltr"
          title="报告详情"
          :with-header="true">
        <api-report :reportData="reportData"/>
      </el-drawer>
    </div>

  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, toRefs} from "vue";
import echartsStatistics from "/@/views/api/Report/components/echartsStatistics.vue";
import ZeroTable from "/@/components/zeroTable/index.vue";
import {ElButton, ElTag} from "element-plus";
import {useReportApi} from "/@/api/useAutoApi/report";
import {getMethodColor, getStatusTag} from "/@/utils/case"


export default defineComponent({
  name: 'apiReportDetail',
  components: {
    ZeroTable,
    echartsStatistics,
  },
  props: {
    report_id: Number,
    start_time: String,
    run_user_name: String,
  },

  setup(props) {
    const state = reactive({
      columns: [
        {label: 'N', columnType: 'index', align: 'center', width: 'auto', showTooltip: false},
        {
          key: 'name', label: '名称', align: 'left', width: '200', showTooltip: true,
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
          key: 'method', label: '请求方法', align: 'center', width: '', showTooltip: true,
          render: (row: any) => row.method ? h(ElTag, {
            type: "",
            style: {"background": getMethodColor(row.method), color: "#ffffff",}
          }, () => row.method) : ""
        },
        {key: 'url', label: 'url', align: 'center', width: '', showTooltip: true},
        {
          key: 'step_type', label: '步骤类型', align: 'center', width: '', showTooltip: true,
          lookupCode: "api_step_type"
        },
        {
          key: 'case_name',
          label: '接口名称',
          width: '',
          align: 'center',
          showTooltip: true,
          lookupCode: 'api_report_run_type'
        },
        {
          key: 'status_code', label: 'HttpCode', width: '', showTooltip: true,
          render: (row: any) => row.status_code ? h(ElTag, {
            type: row.status_code == 200 ? "success" : "warning",
          }, () => row.status_code == 200 ? "200 OK" : row.status_code) : ""
        },
        {
          key: 'run_mode',
          label: '运行模式',
          align: 'center',
          width: '',
          showTooltip: true,
          lookupCode: 'api_report_run_mode'
        },
        // {key: 'has_step_data', label: '子步骤', align: 'center', width: '', showTooltip: true},
        {key: 'case_name', label: '用例名', align: 'center', width: '', showTooltip: true},
        {key: 'run_count', label: '运行数', align: 'center', width: '', showTooltip: true},
        {
          key: 'status', label: 'Status', width: '', showTooltip: true,
          render: (row: any) => h(ElTag, {
            type: getStatusTag(row.status),
          }, () => row.status.toUpperCase())
        },
        {key: 'message', label: '错误信息', width: '', showTooltip: true},
        {
          label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '80',
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

    const getList = () => {
      useReportApi().getReportDetail(state.listQuery).then((res: any) => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
    }

    const getStatistics = () => {
      useReportApi().getReportStatistics(state.statQuery).then((res: any) => {
        state.statisticsData = res.data
      })
    }

    const viewDetail = (row: any) => {
      state.reportData = row
      state.showDetailInfo = true
    }

    const getChildrenData = async (row: any, treeNode: any, resolve: any) => {
      state.listQuery.id = 3
      state.listQuery.parent_step_id = row.step_id
      let res = await useReportApi().getReportDetail(state.listQuery)
      resolve(res.data.rows)
    }

    onMounted(() => {
      state.listQuery.id = props.report_id
      state.statQuery.id = props.report_id
      getList()
      getStatistics()
    })


    return {
      getList,
      getChildrenData,
      viewDetail,
      getMethodColor,
      ...toRefs(state),
    };
  }
})

</script>

<style lang="scss" scoped>

</style>