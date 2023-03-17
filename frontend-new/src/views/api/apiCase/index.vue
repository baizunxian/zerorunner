<template>
  <div class="h100 app-container">
    <el-card>
      <div class="mb15">
        <el-input v-model="listQuery.name" placeholder="请输入用例名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">新增</el-button>
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

    <!--    运行   -->
    <!--    <el-dialog-->
    <!--        draggable-->
    <!--        v-model="showRunPage"-->
    <!--        width="600px"-->
    <!--        top="8vh"-->
    <!--        title="运行用例"-->
    <!--        :close-on-click-modal="false">-->
    <!--      <el-form-->
    <!--          :model="runForm"-->
    <!--          label-width="70px"-->

    <!--      >-->
    <!--        <el-form-item label="运行环境" prop="belong_project_id">-->
    <!--          <el-select v-model="runForm.base_url" placeholder="选择环境" filterable style="width:100%">-->
    <!--            <el-option :value="''" label="自带环境">自带环境</el-option>-->
    <!--            <el-option-->
    <!--                v-for="item in envList"-->
    <!--                :key="item.id"-->
    <!--                :label="item.name"-->
    <!--                :value="item.url">-->
    <!--              <span style="float: left">{{ item.name }}</span>-->
    <!--            </el-option>-->
    <!--          </el-select>-->
    <!--        </el-form-item>-->
    <!--      </el-form>-->
    <!--      <template #footer>-->
    <!--            <span class="dialog-footer">-->
    <!--              <el-button @click="showRunPage = !showRunPage">取消</el-button>-->
    <!--              <el-button type="primary" :loading="runCaseLoading" @click="runTestSuite">运行</el-button>-->
    <!--            </span>-->
    <!--      </template>-->
    <!--    </el-dialog>-->

  </div>
</template>

<script lang="ts">
import {defineComponent, h, onMounted, reactive, ref, toRefs} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";
import {useRouter} from 'vue-router'

export default defineComponent({
  name: 'apiCase',
  setup() {
    const saveOrUpdateRef = ref();
    const router = useRouter();
    const state = reactive({
      columns: [
        {key: 'id', label: 'ID', width: '55', align: 'center', show: true},
        {
          key: 'name', label: '用例名称', width: '', align: 'center', show: true, render: (row: any) => h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenSaveOrUpdate("update", row)
            }
          }, () => row.name)
        },
        {key: 'remarks', label: '用例描述', width: '', align: 'center', show: true},
        {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
        {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
        {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
        {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
        {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
        {
          label: '操作', columnType: 'string', fixed: 'right', width: '200', align: 'center',
          render: (row: any) => h("div", null, [
            h(ElButton, {
              type: "success",
              onClick: () => {
                runTestSuite(row)
              }
            }, () => '运行'),

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
      // list
      listData: [],
      tableLoading: false,
      total: 0,
      listQuery: {
        page: 1,
        pageSize: 20,
        name: '',
      },
      // run
      showRunPage: false,
      runCaseLoading: false,
      runForm: {
        id: null,
        base_url: '',
        run_type: 'suite',
      },

    });
    // 初始化表格数据
    const getList = () => {
      state.tableLoading = true
      useApiCaseApi().getList(state.listQuery)
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
      let query: any = {}
      query.editType = editType
      if (row) query.id = row.id
      router.push({name: 'EditApiCase', query: query})
    };

    // 删除角色
    const deleted = (row: any) => {
      ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      })
          .then(() => {
            useApiCaseApi().deleted({id: row.id})
                .then(() => {
                  ElMessage.success('删除成功');
                  getList()
                })
          })
          .catch(() => {
          });
    };

    //runSuite
    const runTestSuite = (row: any) => {
      state.runForm.id = row.id
      useApiCaseApi().runSuites(state.runForm).then(res => {
        ElMessage.success(res.msg)
      })
    }

    // 页面加载时
    onMounted(() => {
      getList();
    });

    return {
      getList,
      search,
      router,
      saveOrUpdateRef,
      onOpenSaveOrUpdate,
      deleted,
      runTestSuite,
      ...toRefs(state),
    };
  },
});
</script>
