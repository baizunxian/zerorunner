<template>
  <el-card>
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

    <z-table
        :columns="columns"
        :data="listData"
        v-model:page-size="listQuery.pageSize"
        v-model:page="listQuery.page"
        :total="total"
        @pagination-change="getList"
    />

    <report-detail :report-info="reportInfo" ref="reportDetailRef"/>

  </el-card>
</template>

<script setup lang="ts" name="apiReport">

import {useReportApi} from '/@/api/useAutoApi/report';
import {defineComponent, h, onMounted, reactive, toRefs, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus'
import reportDetail from "/@/views/api/Report/components/reportDetail.vue";


export default defineComponent({
  name: 'apiReport',
  components: {
    reportDetail,
  },
  setup() {
    const reportDetailRef = ref()
    const state = reactive({
      columns: [
        {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
        {
          key: 'name', label: '报告名称', align: 'center', width: '', show: true,
          render: (row: any) => h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenReport(row)
            }
          }, () => row.name)
        },
        {
          key: 'status', label: '运行结果', align: 'center', width: '', show: true,
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
        {key: 'run_count', label: '运行数', align: 'center', width: '', show: true},
        // {key: 'successes', label: '执行结果', width: '', showTooltip: true},
        {key: 'run_success_count', label: '成功数', align: 'center', width: '', show: true},
        {key: 'duration', label: '运行耗时(秒)', align: 'center', width: '', show: true},
        {key: 'start_time', label: '运行时间', align: 'center', width: '150', show: true},
        {key: 'run_user_name', label: '执行人', align: 'center', width: '', show: true},
        {
          label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '140',
          render: (row: any) => h("div", null, [
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
        execute_user_name: null,
        responsible_name: null,
        status: null,
        ids: [],
      },
      // report
      reportInfo: {},
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
      state.reportInfo = row
      reportDetailRef.value.showReport()
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
      reportDetailRef,
      ...toRefs(state),
    };
  }
})

</script>

<style lang="scss" scoped>
</style>
