<template>
  <el-card>
    <div class="mb8">
      <div>
        <el-input v-model="state.listQuery.name"
                  placeholder="请输入用例名称"
                  style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="getList">查询</el-button>
      </div>
    </div>

    <z-table
        :columns="state.columns"
        :data="state.listData"
        v-model:page-size="state.listQuery.pageSize"
        v-model:page="state.listQuery.page"
        :total="state.total"
        @pagination-change="getList"
        @selection-change="selectionChange"
    >
    </z-table>
  </el-card>

</template>

<script setup name="SelectCase">
import {onMounted, reactive} from 'vue';
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";
import {ElButton,} from "element-plus";


const state = reactive({
  columns: [
    {label: '选择', columnType: 'selection', width: 'auto', show: true},
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {key: 'id', label: 'ID', width: '55', align: 'center', show: true},
    {key: 'name', label: '用例名称', width: '', align: 'center', show: true,},
    {key: 'remarks', label: '用例描述', width: '', align: 'center', show: true},
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},

  ],
  listData: [],
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
  selectionData: [],
  // run test apiInfo
});
// 初始化表格数据
const getList = () => {
  state.tableLoading = true
  useApiCaseApi().getList(state.listQuery)
      .then((res) => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
        state.tableLoading = false
      })
};

// 选择用例
const selectionChange = (val) => {
  console.log("selectionChange", val)
  state.selectionData = val
}
// 获取选中用例
const getSelectionData = () => {
  return state.selectionData
}

// 页面加载时
onMounted(() => {
  getList();
});

defineExpose({
  getSelectionData
})


</script>

<style lang="scss" scoped>
.file-input-container {
  display: inline-block;
  max-width: 100%;

  .file-input {
    display: flex;
    align-items: center;
    padding: var(--spacing-xs);

    .file-input__native {
      opacity: 0;
      position: absolute;
      width: 0;
      height: 0;
      pointer-events: none;
    }

    .file-input__fake {
      position: relative;
      height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;
      background-color: #F2F2F2;
      min-width: 100px;
      color: #6B6B6B;
      font-weight: 600;

      &:hover {
        color: #212121;
        background-color: #e6e6ee;
      }
    }

    .btn {
      box-sizing: border-box;
      border-radius: 4px;
    }

    .file-input__name {
      box-sizing: border-box;
      display: flex;
      min-width: 0;
      height: 24px;
      align-items: center;
      border-radius: 4px;
      border: 1px solid #E6E6E6;
      font-size: 12px;
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica, Arial, sans-serif;
      color: #212121;
      background-color: transparent;
      padding: 4px 2px;

      .file-input__name__title {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .file-input__name__delete-icon {
        display: flex;
        align-items: center;
        margin-left: 8px;
        padding-right: 2px;
        cursor: pointer;
        color: #212121;
      }
    }
  }
}
</style>