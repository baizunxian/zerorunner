<template>
  <div class="content">
    <div class="block-title">
      <span>关联辅助函数</span>
    </div>
    <div>
      <div>
        <el-button type="primary" link class="" @click="handShowBindPage">
          <el-icon>
            <ele-Plus/>
          </el-icon>
          添加关联
        </el-button>
        <el-button type="primary" link class="" :disabled="state.selectionChangeList.length === 0"
                   @click="unbindFuncs">
          <el-icon>
            <ele-Close/>
          </el-icon>
          取消关联
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          :data="state.bindFuncsList"
          v-model:page-size="state.funcQuery.pageSize"
          v-model:page="state.funcQuery.page"
          :total="state.funcTotal"
          @selection-change="selectionChange"
          @pagination-change="getFuncsList"
      />
    </div>
    <el-dialog
        draggable
        title="关联辅助函数"
        v-model="state.showBindPage"
        width="60%">
      <FuncInfo @selection-change="selectionBindChange"></FuncInfo>
      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary"
                   :disabled="state.selectionBindChangeList.length === 0"
                   @click="bindFuncs">关联</el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup name="FuncsConfig">
import {h, onMounted, reactive} from "vue";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {ElButton, ElMessage} from "element-plus";
import {useFunctionsApi} from "/@/api/useAutoApi/functions";
import {useRouter} from "vue-router";
import FuncInfo from "/@/views/api/functions/index.vue"

const router = useRouter()
const state = reactive({
  env_id: null,
  headersBulk: '',  // bulk内容
  // headers
  headers: [],  // 请求头数据
  bindFuncsList: [],
  // dataSource
  funcList: [],
  funcTotal: 0,
  funcQuery: {
    page: 1,
    pageSize: 20,
    env_id: null,
  },
  columns: [
    {label: '', columnType: 'selection', width: 'auto', show: true},
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {key: 'name', label: '名称', width: '', align: 'center', show: true},
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '80', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "warning",
          onClick: () => {
            viewFuncInfo(row)
          }
        }, () => "查看"),
      ])
    },
  ],
  selectionChangeList: [],

//  bind
  showBindPage: false,
  selectionBindChangeList: [],

});

const setData = (data) => {
  state.env_id = data.id
  getBindFuncsList()
}

const getBindFuncsList = () => {
  useEnvApi().getFuncsByEnvId({env_id: state.env_id})
      .then(res => {
        state.bindFuncsList = res.data
      })
};

// 初始化表格数据
const getFuncsList = () => {
  useFunctionsApi().getList(state.funcQuery)
      .then(res => {
        state.funcList = res.data.rows
        state.funcTotal = res.data.rowTotal
      })
};

const selectionChange = (val) => {
  console.log(val, 1)
  state.selectionChangeList = val
}

const selectionBindChange = (val) => {
  state.selectionBindChangeList = val
}

const handShowBindPage = () => {
  state.showBindPage = true
  getFuncsList()
}
// bindFuncs
const bindFuncs = () => {

  let form = {
    env_id: state.env_id,
    func_ids: state.selectionBindChangeList.map((e) => {
      return e.id
    }),
  }
  useEnvApi().bindingFuncs(form).then((res) => {
    state.showBindPage = false
    ElMessage.success("关联成功!")
    getBindFuncsList()
  })

}

// 解绑函数
const unbindFuncs = () => {
  let form = {
    env_id: state.env_id,
    func_ids: state.selectionChangeList.map((e) => {
      return e.func_id
    }),
  }
  useEnvApi().unbindingFuncs(form).then((res) => {
    ElMessage.success("取消关联成功!")
    getBindFuncsList()
  })
}

// 查看
const viewFuncInfo = (row) => {
  router.push({path: "/api/functions/edit", query: {id: row.func_id}})
};

onMounted(() => {
})

defineExpose({
  setData,
  getFuncsList,
})

</script>


<style lang="scss" scoped>

.block-title {
  display: flex;
  justify-content: space-between;
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 20px;
  line-height: 20px;
  background: #f7f7fc;
  color: #333333;
  border-left: 2px solid #409eff;
  margin-bottom: 5px;
}
</style>