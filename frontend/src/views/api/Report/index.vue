<template>
  <div>
    <el-card shadow="hover">
      <div class="mb15">
        <el-input
            clearable
            v-model="listQuery.name"
            placeholder="输入报告名查询"
            style="width: 200px;"
            class="ml10"
            @keyup.enter.native="search"/>
        <el-input
            clearable
            v-model="listQuery.execute_user_name"
            placeholder="输入执行人查询" style="width: 150px;"
            class="ml10"
            @keyup.enter.native="search"/>

        <el-button class="ml10" type="primary" @click="search">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>

      </div>

      <zero-table
          :columns="columns"
          :data="listData"
          v-model:page-size="listQuery.pageSize"
          v-model:page="listQuery.page"
          :total="total"
          @pagination-change="getList"
      />

      <el-dialog
          draggable
          v-model="showReportDialog"
          width="80%"
          top="8vh"
          title="报告详情"
          destroy-on-close
          :close-on-click-modal="false">
        <template #title>
          <span>报告详情</span>
          <el-button class="ml5" style="font-size: 12px" type="primary" link @click="showLog=!showLog">执行日志</el-button>
        </template>
        <report-detail v-if="report_id"
                       :report_id="report_id"
                       :start_time="start_time"
                       :run_user_name="run_user_name"/>
      </el-dialog>


      <el-dialog
          draggable
          v-model="showLog"
          width="80%"
          top="8vh"
          title="日志"
          destroy-on-close
          :close-on-click-modal="false">
        <pre>{{ report_log }}</pre>
      </el-dialog>
    </el-card>
  </div>

</template>

<script lang="ts">

import {useReportApi} from '/@/api/useAutoApi/report';
import {defineComponent, h, onMounted, reactive, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus'
import reportDetail from "/@/views/api/Report/components/reportDetail.vue";


export default defineComponent({
  name: 'apiReport',
  components: {
    reportDetail,
  },
  setup() {
    const state = reactive({
      columns: [
        {label: '序号', columnType: 'index', align: 'center', width: 'auto', showTooltip: true},
        {
          key: 'name', label: '报告名称', align: 'center', width: '', showTooltip: true,
          render: (row: any) => h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenReport(row)
            }
          }, () => row.name)
        },
        {
          key: 'status', label: '运行结果', align: 'center', width: '', showTooltip: true,
          render: (row: any) => h(ElTag, {
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
        {key: 'run_count', label: '运行数', align: 'center', width: '', showTooltip: true},
        // {key: 'successes', label: '执行结果', width: '', showTooltip: true},
        {key: 'run_success_count', label: '成功数', align: 'center', width: '', showTooltip: true},
        {key: 'duration', label: '运行耗时(秒)', align: 'center', width: '', showTooltip: true},
        {key: 'start_time', label: '运行时间', align: 'center', width: '150', showTooltip: true},
        {key: 'run_user_name', label: '执行人', align: 'center', width: '', showTooltip: true},
        {
          label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '80',
          render: (row: any) => h("div", null, [
            h(ElButton, {
              link: true,
              type: "primary",
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
        execute_user_name: null,
        responsible_name: null,
        status: null,
        ids: [],
      },
      // report
      showLog: false,
      report_id: '',
      start_time: '',
      run_user_name: '',
      report_log: ''
    });

    // 获取列表
    const getList = () => {
      state.tableLoading = true;
      useReportApi().getList(state.listQuery).then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
        state.tableLoading = false
      });
    };

    // 查询
    const search = () => {
      state.listQuery.page = 1
      getList()
    }

    // 删除报告
    const deleted = (row: any) => {
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

    const onOpenReport = (row: any) => {
      state.report_id = row.id
      state.start_time = row.start_time
      state.run_user_name = row.run_user_name
      state.report_log = row.run_log
      state.showReportDialog = !state.showReportDialog
    }

    // 获取列表
    onMounted(() => {
      getList()
    })
    return {
      getList,
      onOpenReport,
      search,
      deleted,
      ...toRefs(state),
    };
  }
})

</script>

<style lang="scss" scoped>
</style>
