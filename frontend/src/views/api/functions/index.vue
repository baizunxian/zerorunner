<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            clearable
            v-model="state.listQuery.name"
            placeholder="函数名称"
            style="width: 200px;"
            class="filter-item"
            @keyup.enter.native="search">

        </el-input>

        <el-button class="ml10" type="primary" @click="search">查询
        </el-button>
        <!--        <el-button class="ml10" type="warning" @click="onOpenSaveOrUpdate(null)">-->
        <!--          公共函数-->
        <!--        </el-button>-->
        <!--        &lt;!&ndash;        函数列表&ndash;&gt;-->
        <!--        <el-button class="ml10" type="success" @click="openFuncList">公共函数列表-->
        <!--        </el-button>-->
      </div>


      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
          @selection-change="selectionChange"
      >
      </z-table>

    </el-card>

    <!--函数列表-->
    <el-dialog
        draggable
        title="函数列表"
        v-model="state.debugFuncListShow"
        width="80%"
        top="8vh">
      <div class="mb15">
        <el-input
            clearable
            v-model="state.funcQuery.func_name"
            placeholder="输入函数名,函数说明查询"
            style="width: 200px;"
            class="filter-item"
            @keyup.enter.native="search"/>

        <el-button class="ml10" type="primary" @click="getFuncList">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>
      </div>
      <!--          函数列表-->
      <el-table
          :data="state.funcList"
          :key="0"
          border
          fit
          highlight-current-row
          style="width: 100%;"
      >
        <el-table-column prop="func_name" label="函数名称" width="180" align="center">
          <template #default="{row}">
            <div style="display: flex; justify-content: space-between">
              <strong>{{ row.func_name }}</strong>
              <span @click="copyFunc(row)">
                  <el-icon>
                    <ele-DocumentCopy/>
                  </el-icon>
                </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="func_args" label="函数参数" width="300" align="left">
          <template #default="{row}">
            <strong>{{ row.func_args }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="func_doc" label="函数说明" :show-overflow-tooltip="true" align="left">
          <template #default="{row}">
            <div v-html="row.func_doc"></div>
          </template>
        </el-table-column>
        <el-table-column prop="" label="操作" width="100" align="center">
          <template #default="{row}">
            <el-button type="primary" @click="showDebugFunc(row)">
              调试
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!--函数调试-->
    <el-dialog
        draggable
        lock-scroll
        title="函数调试"
        v-model="state.debugFuncShow"
        width="80%"
        top="8vh"
        destroy-on-close
        :close-on-click-modal="false"
        append-to-body
    >
      <div>
        <el-descriptions
            class="margin-top"
            :title="state.debugFuncForm.func_parse_str"
            :column="1"
            border
            size="small"
        >
          <template #extra>
            <el-button type="primary" @click="debugFunc">执行</el-button>
          </template>
          <el-descriptions-item label="说明"
                                width="150px">
            <span style="white-space: pre-wrap; font-weight: bold">{{ state.debugFuncForm.func_doc }}</span>
          </el-descriptions-item>
          <el-descriptions-item :label="key"
                                width="150px"
                                v-for="(value, key) in state.funcArgsInfo"
                                :key="value">
            <el-input v-model="state.funcArgsInfo[key]"></el-input>
          </el-descriptions-item>
          <el-descriptions-item width="150px" label="执行结果">
            <z-monaco-editor
                :options="state.options"
                style="height: 300px;"
                v-model:value="state.debugFuncResult"
                v-model:lang="state.lang"
            />
          </el-descriptions-item>
        </el-descriptions>


      </div>
    </el-dialog>
  </div>
</template>

<script setup name="ApiFunctions">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useFunctionsApi} from "/@/api/useAutoApi/functions";
import commonFunction from '/@/utils/commonFunction';
import {useRouter} from 'vue-router'

const emit = defineEmits(["selectionChange"])

const tableRef = ref()
const router = useRouter();
const {copyText} = commonFunction();
const state = reactive({
  columns: [
    {label: '', columnType: 'selection', width: 'auto', align: 'center', show: true},
    {label: '序号', columnType: 'index', width: 'auto', align: 'center', show: true},
    {
      key: 'name', label: '函数名称', width: 'auto', align: 'center', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate(row)
        }
      }, () => row.name)
    },
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
    // {key: 'project_name', label: '所属项目', width: '', align: 'center', show: true},
    // {key: 'module_name', label: '所属模块', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '160', align: 'center',
      render: ({row}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            openFuncList(row)
          }
        }, () => "函数列表"),
        h(ElButton, {
          type: "danger",
          onClick: () => {
            deleted(row)
          }
        }, () => "删除"),
      ])
    },
  ],
  // list
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },

  // funcInfo
  debugFuncResult: null,  // 函数运行结果
  funcList: [],      // 函数列表
  debugFuncListShow: false,
  debugFuncShow: false,
  funcQuery: {
    id: null,
    func_name: '',
  },
  funcArgsInfo: {},  // 函数参数
  debugFuncForm: {
    id: null,
    func_parse_str: '',
    func_name: '',
  },
  // monaco
  options: {
    lineNumbers: 'off',
    // readOnly: true,
    lineDecorationsWidth: 1,
    lineNumbersMinChars: 1,
    minimap: {
      enabled: false
    }
  },
  lang: "python",
  // 选中数据
  selectChangeList: [],

});
// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useFunctionsApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      })
};

// 查询
const search = () => {
  state.listQuery.page = 1
  getList()
}

// 新增或修改
const onOpenSaveOrUpdate = (row) => {
  let query = {}
  if (row) {
    query.id = row.id
  } else {
    query.common = 'common'
  }
  router.push({path: "/api/functions/edit", query: query})
  // saveOrUpdateRef.value.openDialog(editType, row);
};

// 删除角色
const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useFunctionsApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

// 打开函数列表页面
const openFuncList = (row) => {
  state.funcQuery.id = null
  if (row) state.funcQuery.id = row.id
  state.debugFuncListShow = !state.debugFuncListShow
  getFuncList()
}
//获取函数列表
const getFuncList = () => {
  useFunctionsApi().getFuncList(state.funcQuery)
      .then(res => {
        state.funcList = res.data
      })
}
//函数页面初始化
const showDebugFunc = (row) => {
  state.debugFuncResult = ""
  state.funcArgsInfo = {}
  state.funcArgsInfo = row.args_info
  state.debugFuncShow = !state.debugFuncShow
  state.debugFuncForm.func_parse_str = row.func_name + row.func_args
  state.debugFuncForm.func_name = row.func_name
  state.debugFuncForm.func_doc = row.func_doc
  state.debugFuncForm.args_info = state.funcArgsInfo
}
// 函数调试
const debugFunc = () => {
  state.debugFuncResult = ''
  state.debugFuncForm.id = state.funcQuery.id
  useFunctionsApi().debugFunc(state.debugFuncForm)
      .then(res => {
        state.debugFuncResult = JSON.stringify(res.data.result)
        console.log("state.debugFuncResult", state.debugFuncResult)
      })
}

// 复制函数
const copyFunc = (row) => {
  let funcContent = '${' + `${row.func_name}${row.func_args}` + '}'
  funcContent = funcContent.replace(/'/g, '"')
  copyText(funcContent)
}
// 列表选中触发
const selectionChange = (val) => {
  state.selectChangeList = val
  emit("selectionChange", val)
}
// 获取选中数据
const getSelectList = () => {
  return state.selectChangeList
}

defineExpose({
  getSelectList,
})

// 页面加载时
onMounted(() => {
  getList();
});
</script>
