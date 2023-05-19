<template>
  <div class="system-user-container app-container">
    <el-card>
      <div class="system-user-search mb15">
        <el-input v-model="state.listQuery.code" placeholder="请输入编码查询" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdateLookup('save', null)">
          新增
        </el-button>
      </div>

      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      />
    </el-card>

    <!--    编辑数据字典    -->
    <el-dialog
        draggable
        :title="state.lookupEditType === 'save'? `新增` : `修改`"
        v-model="state.isShowLookupDialog"
        top="15vh"
        width="500px">
      <el-form :model="state.lookupForm" :rules="state.lookupRules" ref="lookupFormRef" size="default"
               label-width="90px">
        <el-row :gutter="35">

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="编码" prop="code">
              <el-input v-model="state.lookupForm.code" placeholder="请输入编码" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="描述" prop="description">
              <el-input v-model="state.lookupForm.description" placeholder="请输入描述" clearable></el-input>
            </el-form-item>
          </el-col>

        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.isShowLookupDialog=!state.isShowLookupDialog">取 消</el-button>
          <el-button type="primary" @click="saveOrUpdateLookup">保 存</el-button>
        </span>
      </template>
    </el-dialog>


    <!--    字典管理    -->
    <el-dialog
        title="字典管理"
        v-model="state.isShowLookupValueDialog"
        width="60%"
        draggable
    >
      <div style="display: flex">
        <el-button type="primary" link @click="addLookupValue">
          <el-icon>
            <ele-Plus></ele-Plus>
          </el-icon>
          添加
        </el-button>
      </div>

      <el-table
          border
          :data="state.lookupValueListData"
          v-loading="state.lookupValueTableLoading"
          style="width: 100%"
      >

        <el-table-column label="序号" width="50px" align="center">
          <template #default="scope">
            {{ scope.$index + (state.listQuery.page - 1) * state.listQuery.pageSize + 1 }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="140">
          <template #default="{row}">
            <template v-if="row._edit">
              <el-button
                  size="small"
                  type="primary"
                  @click="saveOrUpdateLookupValue(row)">保存
              </el-button>

              <el-button
                  size="small"
                  type=""
                  @click="row._edit = !row._edit">取消
              </el-button>

            </template>

            <template v-else>
              <el-button
                  size="small"
                  type="primary"
                  @click="editLookupValue(row)">编辑
              </el-button>

              <el-button
                  size="small"
                  type="danger"
                  @click="deletedLookupValue(row)">
                删除
              </el-button>

            </template>


          </template>
        </el-table-column>

        <el-table-column
            v-for="field in state.lookupValueFieldData"
            :key="field.fieldName"
            :label="field.label"
            :align="field.align"
            :width="field.width"
            :show-overflow-tooltip="field.show"
            :prop="field.fieldName"
        >
          <template #default="{row}">
            <template v-if="row._edit">
              <el-input v-if="field.fieldName === 'display_sequence'" v-model.number="row[field.fieldName]"
                        :placeholder="field.label" clearable></el-input>
              <el-input v-else v-model="row[field.fieldName]" :placeholder="field.label" clearable></el-input>
            </template>

            <template v-else>
              {{ row[field.fieldName] }}
            </template>

          </template>
        </el-table-column>

      </el-table>

    </el-dialog>

  </div>
</template>

<script lang="ts" setup name="SystemLookup">
import {h, nextTick, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import {useLookupApi} from '/@/api/useSystemApi/lookup';
import {formatLookup} from "/@/utils/lookup";


const lookupFormRef = ref();
const tableRef = ref();
// const store = useStore();
// const lookupInfo = store.state.lookup.lookup;
const state = reactive({
  columns: [
    {
      key: 'code', label: '编码', width: '', align: 'center', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdateLookup("update", row)
        }
      }, () => row.code)
    },
    {key: 'description', label: '描述', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
    {key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
    {key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'left', align: 'center', width: '220',
      render: (row: any) => h("div", null, [
        h(ElButton, {
          type: "success",
          onClick: () => {
            onOpenSaveOrUpdateLookupValuePage(row)
          }
        }, () => '字典管理'),

        h(ElButton, {
          type: "primary",
          onClick: () => {
            onOpenSaveOrUpdateLookup("update", row)
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
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    code: '',
  },
  // lookup
  lookupEditType: 'save',
  isShowLookupDialog: false,
  lookupForm: {
    id: null,
    code: '',
    description: ''
  },
  lookupRules: {
    code: [{required: true, message: '请输入编码', trigger: 'blur'},],
    description: [{required: true, message: '请输入描述', trigger: 'blur'},],
  },

  //lookup value
  lookupValueListData: [],
  lookupValueTableLoading: false,
  isShowLookupValueDialog: false,
  lookupValueFieldData: [
    {fieldName: 'lookup_code', label: '编码', width: '', align: 'center', show: true},
    {fieldName: 'lookup_value', label: '值', width: '', align: 'center', show: true},
    {fieldName: 'display_sequence', label: '显示顺序', width: '150', align: 'center', show: true},
    {fieldName: 'ext', label: '扩展', width: '', align: 'center', show: true},
  ],
  lookupValueQuery: {
    code: '',
    lookup_id: '',
  },
  lookupValueForm: {
    id: null,
    code: '',
    description: ''
  }
});
// 获取数据字典列表
const getList = () => {
  tableRef.value.openLoading()
  useLookupApi().getLookupList(state.listQuery)
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

// 新增或修改字典
const onOpenSaveOrUpdateLookup = (editType: string, row: any) => {
  state.lookupEditType = editType
  if (row) {
    state.lookupForm.id = row.id
    state.lookupForm.code = row.code
    state.lookupForm.description = row.description
  } else {
    state.lookupForm = {}
  }
  state.isShowLookupDialog = !state.isShowLookupDialog
  nextTick(() => {
    lookupFormRef.value.clearValidate()
  })
};

const saveOrUpdateLookup = () => {
  lookupFormRef.value.validate((valid: any) => {
    if (valid) {
      useLookupApi().saveOrUpdateLookup(state.lookupForm)
          .then(() => {
            ElMessage.success('操作成功');
            getList()
            state.isShowLookupDialog = !state.isShowLookupDialog
          })
    }
  })
}

// 删除
const deleted = (row: any) => {
  ElMessageBox.confirm('此操作将永久删除, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useLookupApi().delLookup({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
      })
      .catch(() => {
      });
};

// 获取字典值列表
const getLookupValueList = () => {
  state.lookupValueTableLoading = true
  useLookupApi().getLookupValue(state.lookupValueQuery)
      .then(res => {
        state.lookupValueListData = res.data
        state.lookupValueTableLoading = false
      })
};
// 新增或修改字典值
const onOpenSaveOrUpdateLookupValuePage = (row: any) => {
  state.lookupValueQuery.code = row.code
  state.lookupValueQuery.lookup_id = row.id
  state.isShowLookupValueDialog = !state.isShowLookupValueDialog
  getLookupValueList()
};

const editLookupValue = (row: any) => {
  row._edit = !row._edit
};

const addLookupValue = () => {
  let lookupValue: object = {
    id: null,
    lookup_id: state.lookupValueQuery.lookup_id,
    lookup_code: '',
    lookup_value: '',
    display_sequence: '',
    ext: '',
    _edit: true,
  }
  state.lookupValueListData.push(lookupValue)
}

const saveOrUpdateLookupValue = (row: any) => {
  useLookupApi().saveOrUpdateLookupValue(row)
      .then((res: any) => {
        ElMessage.success('保存成功！');
        row._edit = false
        row.id = res.data?.id
        // getLookupValueList()
      })
}

const deletedLookupValue = (row: any) => {
  ElMessageBox.confirm('此操作将永久删除, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useLookupApi().delLookupValue({id: row.id})
            .then(() => {
              ElMessage.success('操作成功！');
              getLookupValueList()
            })
      })
      .catch(() => {
      });
}

// 页面加载时
onMounted(() => {
  getList();
  console.log(formatLookup('test', '80'))
});
</script>

<style lang="scss" scoped>
.auto-test.el-dialog {
  height: 90%;
  margin-top: 8vh !important;
  color: yellowgreen;
}
</style>