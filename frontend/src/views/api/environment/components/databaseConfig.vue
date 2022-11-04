<template>
  <div class="content">
    <div class="block-title">添加数据库</div>
    <div style="padding: 10px 0">
      <el-form :model="form" :rules="dataSourceRules" ref="formRef" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="数据源名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入数据源名称" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="数据源类型" prop="type">
              <el-select v-model="form.type" clearable placeholder="选择数据源类型" style="width: 100%">
                <el-option
                    v-for="item in dataSourceType"
                    :key="item"
                    :label="item"
                    :value="item"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="地址" prop="host">
              <el-input v-model="form.host" placeholder="请输入地址" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="端口" prop="port">
              <el-input v-model.number="form.port" placeholder="请输入端口" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="用户名" prop="user">
              <el-input v-model="form.user" placeholder="请输入用户名" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="密码">
              <el-input v-model="form.password" placeholder="请输入密码" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <div class="block-title">关联数据库</div>

    <div>
      <zero-table
          :columns="columns"
          :data="dataSourceList"
          v-model:page-size="dataSourceQuery.pageSize"
          v-model:page="dataSourceQuery.page"
          :total="dataSourceTotal"
          @pagination-change="getDataSourceList"
      />
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from "vue";
import {Search} from '@element-plus/icons-vue'
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: 'databaseConfig',
  components: {},
  setup() {
    const formRef = ref()
    const state = reactive({
      form: {
        id: null,
        name: "",
        type: "mysql",
        host: "",
        port: "",
        user: "",
        password: "",
        env_id: "",
      },
      headersBulk: '',  // bulk内容
      // headers
      headers: [],  // 请求头数据

      // dataSource
      dataSourceType: ['mysql'],
      dataSourceList: [],
      dataSourceTotal: 0,
      dataSourceQuery: {
        page: 1,
        pageSize: 1000,
        env_id: null,
      },
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
      ],
      dataSourceRules: {
        name: [{required: true, message: '请输入数据源名称', trigger: 'blur'},],
        host: [{required: true, message: '请选数据源地址', trigger: 'blur'},],
        env_id: [{required: true, message: '请选择环境', trigger: 'blur'},],
        port: [{required: true, message: '请输入端口号', trigger: 'blur'},],
      },

    });

    const setData = (data: any) => {
      console.log(data, 'data----->')
      if (data?.id) {
        state.form.env_id = data?.id
        getDataSourceList()
      }
    }

    // 初始化表格数据
    const getDataSourceList = () => {
      state.dataSourceQuery.env_id = state.form.env_id
      useQueryDBApi().getSourceList(state.dataSourceQuery)
          .then(res => {
            state.dataSourceList = res.data.rows
            state.dataSourceTotal = res.data.rowTotal
          })
    };

    // 新增
    const saveOrUpdate = () => {
      formRef.value.validate((valid: any) => {
        if (valid) {
          useQueryDBApi().saveOrUpdate(state.form)
              .then((res: any) => {
                ElMessage.success('操作成功');
                state.dataSourceList.push(res.data)
              })
        }
      })
    };

    onMounted(() => {

    })

    return {
      Search,
      formRef,
      setData,
      getDataSourceList,
      saveOrUpdate,
      ...toRefs(state),
    };
  },
})

</script>


<style lang="scss" scoped>

.block-title {
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