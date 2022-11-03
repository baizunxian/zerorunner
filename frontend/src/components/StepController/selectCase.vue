<template>
  <div>
    <el-card shadow="hover">
      <div class="mb8">
        <div>
          <el-input v-model="listQuery.name" placeholder="请输入用例名称" style="max-width: 180px"></el-input>
          <el-button type="primary" class="ml10" @click="getList">
            <el-icon>
              <ele-Search/>
            </el-icon>
            查询
          </el-button>
        </div>
      </div>

      <zero-table
          :columns="columns"
          :data="listData"
          v-model:page-size="listQuery.pageSize"
          v-model:page="listQuery.page"
          :total="total"
          @pagination-change="getList"
          @selection-change="selectionChange"
      >
      </zero-table>
    </el-card>

  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, toRefs} from 'vue';
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";
import {ElTag} from "element-plus";


export default defineComponent({
  name: 'selectTestCase',
  setup() {
    const state = reactive({
      columns: [
        {label: '序号', columnType: 'selection', width: 'auto', showTooltip: true},
        {label: '序号', columnType: 'index', width: 'auto', showTooltip: true},
        {key: 'id', label: 'ID', columnType: 'string', width: 'auto', showTooltip: true},
        {key: 'name', label: '用例名', width: '', showTooltip: true},
        {
          key: 'method', label: '请求方式', width: '', showTooltip: true,
          render: (row: any) => h(ElTag, {
            type: "",
            style: {"background": getMethodColor(row.method), color: "#ffffff",}
          }, row.method)
        },
        {key: 'project_name', label: '所属项目', width: 'auto', showTooltip: true},
        {key: 'module_name', label: '所属模块', width: 'auto', showTooltip: true},
        {key: 'updation_date', label: '更新时间', width: '150', showTooltip: true},
        {key: 'updated_by_name', label: '更新人', width: 'auto', showTooltip: true},
        {key: 'creation_date', label: '创建时间', width: '150', showTooltip: true},
        {key: 'created_by_name', label: '创建人', width: 'auto', showTooltip: true},

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
      // run test apiCase
    });
    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useApiCaseApi().getList(state.listQuery)
          .then((res: any) => {
            state.listData = res.data.rows
            state.total = res.data.rowTotal
            state.tableLoading = false
          })
    };

    // 选择用例
    const selectionChange = (val: any) => {
      console.log("selectionChange", val)
      state.selectionData = val
    }
    // 获取选中用例
    const getSelectionData = () => {
      return state.selectionData
    }

    // 获取请求方式tag颜色
    const getMethodColor = (method: string) => {
      let color = ""
      if (method == "GET") {
        color = "#61affe"
      } else if (method == "POST") {
        color = "#49cc90"
      } else if (method == "DELETE") {
        color = "#f93e3d"
      } else if (method == "PUT") {
        color = "#fca130"
      }
      return color
    }
    // 页面加载时
    onMounted(() => {
      getList();
    });
    return {
      getList,
      selectionChange,
      getSelectionData,
      ...toRefs(state),
    };
  },
});
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
        background-color: #E6E6E;
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