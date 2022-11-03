<template>
  <div>
    <el-card shadow="hover">
      <div class="mb15">
        <el-input v-model="listQuery.name" :placeholder="`请输入环境名称`" style="max-width: 180px"></el-input>
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
      />
    </el-card>
    <save-or-update ref="saveOrUpdateRef" @getList="getList"/>
  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import saveOrUpdate from "/@/views/tools/dataSource/components/saveOrUpdate.vue";


export default defineComponent({
  name: 'dataSource',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
    const state = reactive({
      columns: [
        {label: '序号', columnType: 'index', width: 'auto', showTooltip: true},
        {key: 'name', label: '数据源名称', width: '', align: 'center', showTooltip: true},
        {key: 'env_name', label: '所属环境', width: '', align: 'center', showTooltip: true},
        {key: 'type', label: '类型', width: '', align: 'center', showTooltip: true},
        {key: 'host', label: '地址', width: '', align: 'center', showTooltip: true},
        {key: 'port', label: '端口', width: '', align: 'center', showTooltip: true},
        {key: 'user', label: '用户名', width: '', align: 'center', showTooltip: true},
        {key: 'updation_date', label: '更新时间', width: '150', align: 'center', showTooltip: true},
        {key: 'updated_by_name', label: '更新人', width: '', align: 'center', showTooltip: true},
        {key: 'creation_date', label: '创建时间', width: '150', align: 'center', showTooltip: true},
        {key: 'created_by_name', label: '创建人', width: '', align: 'center', showTooltip: true},
        {
          label: '操作', fixed: 'right', width: '100',
          render: (row: any) => h("div", null, [
            h(ElButton, {
              link: true,
              type: "primary",
              onClick: () => {
                onOpenSaveOrUpdate("update", row)
              }
            }, '编辑'),

            h(ElButton, {
              link: true,
              type: "primary",
              onClick: () => {
                deleted(row)
              }
            }, '删除')
          ])
        },
      ],
      // list
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
      useQueryDBApi().getSourceList(state.listQuery)
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
            useQueryDBApi().deletedSource({id: row.id})
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
