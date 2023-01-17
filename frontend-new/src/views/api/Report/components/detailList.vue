<template>
  <div class="">
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
  </div>
</template>

<script lang="ts" setup name="ReportDetailList">
import {h, onMounted, reactive} from "vue";
import {ElButton, ElTag} from "element-plus";
import {useReportApi} from "/@/api/useAutoApi/report";
import {getMethodColor} from "/@/utils/case"


const state = reactive({
  columns: [
    {label: 'N', columnType: 'index', align: 'center', width: 'auto', show: false},
    {
      key: 'name', label: '名称', align: 'left', width: '200', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          viewDetail(row)
        }
      }, () => row.name)
    },
    {
      key: 'step_tag', label: '步骤类型', align: 'center', width: '', show: true,
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
      key: 'run_mode',
      label: '运行模式',
      align: 'center',
      width: '',
      show: true,
      lookupCode: 'api_report_run_mode'
    },
    {key: 'has_step_data', label: '子步骤', align: 'center', width: '', show: true},
    {key: 'case_name', label: '用例名', align: 'center', width: '', show: true},
    {
      key: 'method', label: '请求方法', align: 'center', width: '', show: true,
      render: (row: any) => row.method ? h(ElTag, {
        type: "",
        style: {"background": getMethodColor(row.method), color: "#ffffff",}
      }, () => row.method) : ""
    },
    {key: 'url', label: 'url', align: 'center', width: '', show: true},
    {key: 'run_count', label: '运行数', align: 'center', width: '', show: true},
    {key: 'success', label: '是否成功', width: '', show: true},
    {key: 'status', label: 'Status', width: '', show: true},
    {key: 'message', label: '错误信息', width: '', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: 'auto',
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
})

const getList = () => {
  state.listQuery.id = 3
  useReportApi().getReportDetail(state.listQuery).then((res: any) => {
    state.listData = res.data.rows
    state.total = res.data.rowTotal
  })
}


const viewDetail = () => {

}

const getChildrenData = async (row: any, treeNode: any, resolve: any) => {
  state.listQuery.id = 3
  state.listQuery.parent_step_id = row.step_id
  let res = await useReportApi().getReportDetail(state.listQuery)
  resolve(res.data.rows)
}

onMounted(() => {
  getList()
})


</script>

<style lang="scss" scoped>

</style>