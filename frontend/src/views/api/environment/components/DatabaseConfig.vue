<template>
  <div class="content">
    <div class="block-title">
      <span>关联数据库</span>
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
                   @click="unbindDataSource">
          <el-icon>
            <ele-Close/>
          </el-icon>
          取消关联
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          :data="state.bindDataSourceList"
          v-model:page-size="state.dataSourceQuery.pageSize"
          v-model:page="state.dataSourceQuery.page"
          :total="state.dataSourceTotal"
          @selection-change="selectionChange"
          @pagination-change="getDataSourceList"
      />
    </div>
    <el-dialog
        draggable
        title="关联数据源"
        v-model="state.showBindPage"
        width="60%">
      <DataSource @selectionChange="selectionSourceChange"></DataSource>
      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary"
                   :disabled="state.selectionBindChangeList.length === 0"
                   @click="bindDataSource">
          关联
        </el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup name="DatabaseConfig">
import {onMounted, reactive} from "vue";
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {ElMessage} from "element-plus";
import DataSource from "/@/views/api/dataSource/index.vue"


const state = reactive({
  env_id: null,
  headersBulk: '',  // bulk内容
  // headers
  headers: [],  // 请求头数据
  bindDataSourceList: [],
  // dataSource
  dataSourceList: [],
  dataSourceTotal: 0,
  dataSourceQuery: {
    page: 1,
    pageSize: 20,
    env_id: null,
  },
  columns: [
    {label: '', columnType: 'selection', width: 'auto', show: true},
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {key: 'name', label: '数据源名称', width: '', align: 'center', show: true},
    {key: 'env_name', label: '所属环境', width: '', align: 'center', show: true},
    {key: 'type', label: '类型', width: '', align: 'center', show: true},
    {key: 'host', label: '地址', width: '', align: 'center', show: true},
    {key: 'port', label: '端口', width: '', align: 'center', show: true},
    {key: 'user', label: '用户名', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
  ],
  selectionChangeList: [],

//  bind
  showBindPage: false,
  selectionBindChangeList: [],

});

const setData = (data) => {
  state.env_id = data.id
  getBindDateSourceList()
}

const getBindDateSourceList = () => {
  useEnvApi().getDataSourceByEnvId({env_id: state.env_id})
      .then(res => {
        state.bindDataSourceList = res.data
      })
};

// 初始化表格数据
const getDataSourceList = () => {
  useQueryDBApi().getSourceList(state.dataSourceQuery)
      .then(res => {
        state.dataSourceList = res.data.rows
        state.dataSourceTotal = res.data.rowTotal
      })
};

const selectionChange = (val) => {
  console.log(val, 1)
  state.selectionChangeList = val
}

const selectionSourceChange = (val) => {
  state.selectionBindChangeList = val
}

const handShowBindPage = () => {
  state.showBindPage = true
  getDataSourceList()
}
// bindDataSource
const bindDataSource = () => {

  let form = {
    env_id: state.env_id,
    data_source_ids: state.selectionBindChangeList.map((e) => {
      return e.id
    }),
  }
  useEnvApi().bindingDataSource(form).then((res) => {
    state.showBindPage = false
    ElMessage.success("关联成功!")
    getBindDateSourceList()
  })

}

const unbindDataSource = () => {
  let form = {
    env_id: state.env_id,
    data_source_ids: state.selectionChangeList.map((e) => {
      return e.data_source_id
    }),
  }
  useEnvApi().unbindingDataSource(form).then((res) => {
    ElMessage.success("取消关联成功!")
    getBindDateSourceList()
  })
}

onMounted(() => {
})

defineExpose({
  setData,
  getDataSourceList,
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