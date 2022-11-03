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
        <!--      <el-select v-model="listQuery.status" placeholder="运行结果" style="width: 150px;"-->
        <!--                 class="filter-item">-->
        <!--        <el-option-->
        <!--            v-for="item in options"-->
        <!--            :key="item.value"-->
        <!--            :label="item.label"-->
        <!--            :value="item.value">-->
        <!--        </el-option>-->
        <!--      </el-select>-->
        <!--        <el-date-picker-->
        <!--            v-model="listQuery.min_and_max"-->
        <!--            type="datetimerange"-->
        <!--            align="right"-->
        <!--            start-placeholder="起始日期"-->
        <!--            end-placeholder="截止日期"-->
        <!--            style="width: 340px;"-->
        <!--            value-format="yyyy-MM-dd HH:mm:ss"-->
        <!--            class="filter-item"-->
        <!--            :default-time="['00:00:00', '23:59:59']">-->
        <!--        </el-date-picker>-->
        <el-button class="ml10" type="primary" @click="search">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>

      </div>

      <!--      <el-table-->
      <!--          v-loading="tableLoading"-->
      <!--          :data="listData"-->
      <!--          stripe-->
      <!--          border-->
      <!--          fit-->
      <!--          highlight-current-row-->
      <!--          style="width: 100%;"-->
      <!--      >-->
      <!--        <el-table-column type="selection" width="40"></el-table-column>-->
      <!--        <el-table-column label="序号" width="45px" align="center">-->
      <!--          <template #default="scope">-->
      <!--            {{ scope.$index + (listQuery.page - 1) * listQuery.pageSize + 1 }}-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column-->
      <!--            v-for="field in fieldData"-->
      <!--            :key="field.fieldName"-->
      <!--            :label="field.label"-->
      <!--            :align="field.align"-->
      <!--            :width="field.width"-->
      <!--            :show-overflow-tooltip="field.show"-->
      <!--            :prop="field.fieldName"-->
      <!--        >-->
      <!--          <template #default="{row}">-->
      <!--            <template v-if="field.fieldName === 'name'">-->
      <!--              <el-button size="small"-->
      <!--                         type="primary" link-->
      <!--                         @click="onOpenReport(row)">-->
      <!--                {{ row[field.fieldName] }}-->
      <!--              </el-button>-->
      <!--            </template>-->

      <!--            <template v-else-if="field.fieldName === 'status'">-->
      <!--              <el-tag type="success" v-if="row.success">通过</el-tag>-->
      <!--              <el-tag type="danger" v-else>不通过</el-tag>-->
      <!--            </template>-->

      <!--            <template v-else>-->
      <!--              <span>{{ field.lookupCode?formatLookup(field.lookupCode, row[field.fieldName]): row[field.fieldName]  }}</span>-->
      <!--            </template>-->

      <!--          </template>-->
      <!--        </el-table-column>-->

      <!--        <el-table-column label="操作" align="center" width="80" fixed="right">-->
      <!--          <template #default="{row}">-->
      <!--            <el-button type="primary" link @click="deleteReport(row)">-->
      <!--              删除-->
      <!--            </el-button>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--      </el-table>-->
      <!--      <pagination :total="total"-->
      <!--                  :hidden="total === 0"-->
      <!--                  v-model:page="listQuery.page"-->
      <!--                  v-model:limit="listQuery.pageSize"-->
      <!--                  @pagination="getList"/>-->

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
        <test-report :reportBody="reportBody"/>
      </el-dialog>
    </el-card>
  </div>

</template>

<script lang="ts">

import TestReport from '/@/views/api/Report/components/report.vue';
import {useReportApi} from '/@/api/useAutoApi/report';
import {defineComponent, h, onMounted, reactive, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus'


export default defineComponent({
  name: 'apiReport',
  components: {TestReport},
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
        {key: 'run_test_count', label: '运行用例', align: 'center', width: '', showTooltip: true},
        // {key: 'successes', label: '执行结果', width: '', showTooltip: true},
        {key: 'successful_use_case', label: '成功用例', align: 'center', width: '', showTooltip: true},
        {key: 'duration', label: '执行耗时(秒)', align: 'center', width: '', showTooltip: true},
        {key: 'start_at', label: '执行时间', align: 'center', width: '150', showTooltip: true},
        {key: 'execute_user_name', label: '执行人', align: 'center', width: '', showTooltip: true},
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
      reportBody: {},
      reportID: '',
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
      useReportApi().getReportById({id: row.id})
          .then((res: any) => {
            state.reportBody = res.data.report_body
            state.showReportDialog = !state.showReportDialog
          })
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
.employee_body {
  margin: 10px 20px 0;
  overflow: hidden;
}

.inputclass {
  width: 300px;
}

.el-dialog {
  height: 50%;
}

table {
  width: 50%;
  border-collapse: collapse;

  tr, td {
    border: 1px solid #d2d2d6;
    padding: 5px;
  }
}

.filter-container {
  .filter-item {
    margin-right: 10px;
  }
}

:deep(.el-dialog--center .el-dialog__body) {
  padding: 5px;
}
</style>

<style lang="css"> .el-tooltip__popper {
  max-width: 20%
} </style>