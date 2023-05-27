<template>
  <div class="app-container">
    <el-card>
      <UiPageInfo></UiPageInfo>
      <UiElement></UiElement>
    </el-card>

  </div>
</template>

<script setup lang="ts" name="EditPage">
import {ElButton} from "element-plus";
import {h, reactive, ref} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import UiPageInfo from "/@/views/ui/page/uiPageInfo.vue";
import UiElement from "/@/views/ui/page/uiElement.vue";

const tableRef = ref()

const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {
      key: 'name', label: '模块名称', width: '', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    {key: 'test_user', label: '测试人员', width: '', align: 'center', show: true},
    {key: 'dev_user', label: '开发人员', width: '', align: 'center', show: true},
    {key: 'case_count', label: '用例数', width: '', align: 'center', show: true},
    {key: 'simple_desc', label: '描述', width: '', align: 'center', show: true},
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
    {key: 'config_id', label: '关联配置', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: (row: any) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenSaveOrUpdate("update", row)
          }
        }, () => '编辑'),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deleted(row)
          }
        }, () => '删除')
      ])
    },
  ],
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
//
  form: {},
});

const getElementList = () => {
  tableRef.value.openLoading()
  useUiPageApi().getList(state.listQuery)
    .then((res: any) => {
      state.listData = res.data.list;
      state.total = res.data.total;

    })
    .finally(() => {
      tableRef.value.closeLoading()
    })
}
</script>

<style scoped lang="scss">

.api-case {
  padding: 15px 16px;
  background-color: #ffffff;
  border-radius: 10px;
  border-left: 5px solid #409eff;
  margin-bottom: 20px;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);

  .api-case__url_info {
    display: flex;
    margin-bottom: 20px;
  }

  :deep(.input-with-select .el-input-group__prepend) {
    background-color: var(--el-fill-color-blank);
  }
}

</style>