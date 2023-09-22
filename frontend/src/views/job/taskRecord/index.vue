<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input class="ml10" v-model="state.listQuery.task_id" clearable placeholder="任务id查询" style="max-width: 180px"></el-input>
        <el-input class="ml10" v-model="state.listQuery.trace_id" clearable placeholder="trace_id查询" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
        </el-button>
<!--        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增-->
<!--        </el-button>-->
      </div>
      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      >
      </z-table>
    </el-card>
  </div>
</template>

<script setup name="uiCase">
import {ElButton, ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive, ref} from "vue";
import {useUiCaseApi} from "/@/api/useUiApi/uiCase";
import {useRouter} from 'vue-router'
import {useTaskRecordApi} from "/@/api/useJobApi/taskRecord";

const props = defineProps({
  business_id: {
    type: String,
    default: ''
  },
  task_type: {
    type: Number,
    default: null
  }
})

const tableRef = ref();
const router = useRouter();

const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    // {key: 'task_name', label: '执行方法', width: '', align: 'center', show: true},
    {key: 'task_id', label: '任务id', width: '', align: 'center', show: true},
    {key: 'status', label: '状态', width: '', align: 'center', show: true},
    {key: 'result', label: '结果', width: '', align: 'center', show: true},
    {key: 'traceback', label: '错误信息', width: '', align: 'center', show: true},
    {key: 'business_id', label: '业务id', width: '', align: 'center', show: true},
    {key: 'start_time', label: '开始时间', width: '150', align: 'center', show: true},
    {key: 'end_time', label: '结束时间', width: '150', align: 'center', show: true},
    {key: 'trace_id', label: 'trace_id', width: '150', align: 'center', show: true},
  ],
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    business_id: '',
    task_type: null,
    task_id: '',
    trace_id: '',
  },
});

const search = () => {
  state.listQuery.page = 1
  getList()
};

const getList = () => {
  if (props.business_id) {
    state.listQuery.business_id = props.business_id
  }
  if (props.task_type) {
    state.listQuery.task_type = props.task_type
  }
  tableRef.value.openLoading()
  useTaskRecordApi().getTaskList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows;
      state.total = res.data.rowTotal;

    })
    .finally(() => {
      tableRef.value.closeLoading()
    })
};

// 运行
const runUiCase = (row) => {
  useUiCaseApi().runUiCaseById({id: row.id}).then((res => {
    ElMessage.success('运行成功');
  }))
};

// 新增或修改
const onOpenSaveOrUpdate = (editType, row) => {
  let query = {}
  query.editType = editType
  if (row) query.id = row.id
  router.push({name: 'editUiCase', query: query})
};


// 删除
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      useUiCaseApi().deleted({id: row.id})
        .then(() => {
          ElMessage.success('删除成功');
          getList()
        })
    })
    .catch(() => {
    });
};

// 页面加载时
onMounted(() => {
  getList();
});

</script>

<style scoped lang="scss">

</style>