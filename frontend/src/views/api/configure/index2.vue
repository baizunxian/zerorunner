<template>
  <div>
    <el-card>
      <div class="mb15">
        <el-input v-model="listQuery.name" placeholder="请输入配置名称" style="max-width: 180px"></el-input>
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
      <z-table
          :columns="columns"
          :data="listData"
          v-model:page-size="listQuery.pageSize"
          v-model:page="listQuery.page"
          :total="total"
          @pagination-change="getList"
      />
    </el-card>

    <el-dialog
        draggable
        v-model="showSaveOrUpdate"
        width="80%"
        top="8vh"
        :title="editType === 'save'? '新增配置':'更新配置'"
        destroy-on-close
        :close-on-click-modal="false">
      <save-or-update ref="saveOrUpdateRef" @getList="getList" :config_id="config_id"/>
      <template #footer>
        <el-button @click="showSaveOrUpdate = false">取 消</el-button>
        <el-button type="primary" @click="saveOrUpdate">保 存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useTestCaseApi} from "/@/api/useAutoApi/testCase";
import {useRouter} from "vue-router";
import saveOrUpdate from '/@/views/api/configure/components/saveOrUpdate.vue';

export default defineComponent({
  name: 'apiConfigure',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
    const router = useRouter();
    const state = reactive({
      columns: [
        {label: '序号', columnType: 'index', width: 'auto', show: true},
        {
          key: 'name', label: '配置名称', width: '', show: true,
          render: ({row}: any) => h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenSaveOrUpdate("update", row)
            }
          }, () => row.name)
        },
        {key: 'project_name', label: '所属项目', width: '', show: true},
        {key: 'module_name', label: '所属模块', width: '', show: true},
        {key: 'updation_date', label: '更新时间', width: '150', show: true},
        {key: 'updated_by_name', label: '更新人', width: '', show: true},
        {key: 'creation_date', label: '创建时间', width: '150', show: true},
        {key: 'created_by_name', label: '创建人', width: '', show: true},
        {
          label: '操作', fixed: 'right', width: 'auto',
          render: ({row}: any) => h("div", null, [
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
        case_type: 2,
        name: '',
      },
      // configure
      editType: 'save',
      config_id: null,
      showSaveOrUpdate: false,
    });
    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useTestCaseApi().getList(state.listQuery)
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

    // 新增或修改
    const onOpenSaveOrUpdate = (editType: string, row: any | null) => {
      state.editType = editType
      if (row && row.id) {
        state.config_id = row.id
      } else {
        state.config_id = null
      }
      state.showSaveOrUpdate = !state.showSaveOrUpdate
      // router.push({name: 'saveOrUpdateTestCase', query: query})
    };

    // saveOrUpdate
    const saveOrUpdate = () => {
      saveOrUpdateRef.value.saveOrUpdate()
    };

    // 删除角色
    const deleted = (row: any) => {
      ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      })
          .then(() => {
            useTestCaseApi().deleted({id: row.id})
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
      saveOrUpdate,
      onOpenSaveOrUpdate,
      deleted,
      router,
      ...toRefs(state),
    };
  },
});
</script>
