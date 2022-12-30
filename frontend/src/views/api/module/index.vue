<template>
  <el-card>
    <div class="mb15">
      <el-input v-model="listQuery.name" placeholder="请输入模块名称" style="max-width: 180px"></el-input>
      <el-button type="primary" class="ml10" @click="search">
        <el-icon>
          <ele-Search/>
        </el-icon>
        查询
      </el-button>
      <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
        <el-icon>
          <ele-FolderAdd/>
        </el-icon>
        新增
      </el-button>
    </div>
    <zero-table
        :columns="columns"
        :data="listData"
        v-model:page-size="listQuery.pageSize"
        v-model:page="listQuery.page"
        :total="total"
        @pagination-change="getList"
    >
    </zero-table>
  </el-card>
  <save-or-update ref="saveOrUpdateRef" @getList="getList"/>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import saveOrUpdate from '/@/views/api/module/components/saveOrUpdate.vue';
import {useModuleApi} from "/@/api/useAutoApi/module";

export default defineComponent({
  name: 'apiModule',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
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
      tableLoading: false,
      total: 0,
      listQuery: {
        page: 1,
        pageSize: 20,
        name: '',
      },
    });
    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useModuleApi().getList(state.listQuery)
          .then(res => {
            state.listData = res.data.rows
            state.total = res.data.rowTotal
            state.tableLoading = false
          })
    };

    // 查询
    const search = () => {
      state.listQuery.page = 1
      getList()
    }

    // 新增或修改角色
    const onOpenSaveOrUpdate = (editType: string, row: any) => {
      saveOrUpdateRef.value.openDialog(editType, row);
    };

    // 删除角色
    const deleted = (row: any) => {
      ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      })
          .then(() => {
            useModuleApi().deleted({id: row.id})
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
    return {
      getList,
      search,
      saveOrUpdateRef,
      onOpenSaveOrUpdate,
      deleted,
      ...toRefs(state),
    };
  },
});
</script>
