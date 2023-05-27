<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between">
        <strong>元素管理</strong>
        <div>
          <el-button type="primary" @click="addElement" :disabled="!props.pageId">添加元素</el-button>
        </div>
      </div>
    </template>

    <el-table
        :data="state.elementList"
    >
      <template v-for="(col, index) in state.columns" :key="col.key">

        <el-table-column
            v-if="col.key === 'location_type'"
            :show-overflow-tooltip="col.show"
            :label="col.label"
            :sortable="col.sortable"
            :prop="col.key"
            :fixed="col.fixed"
            :align="col.align"
            :width="col.width">
          <template #default="{row}">
            <el-select v-model="row.location_type" placeholder="请选择" style="width:100%"
                       v-if="row._edit">
              <el-option
                  v-for="type in state.locationTypes"
                  :key="type.value"
                  :label="type.label"
                  :value="type.value">
              </el-option>
            </el-select>
            <span v-else>{{ row[col.key] }}</span>
          </template>
        </el-table-column>

        <el-table-column
            v-else
            :show-overflow-tooltip="col.show"
            :label="col.label"
            :sortable="col.sortable"
            :prop="col.key"
            :fixed="col.fixed"
            :align="col.align"
            :width="col.width">
          <template #default="{row}">
            <el-input v-if="row._edit" v-model="row[col.key]"></el-input>
            <span v-else>{{ row[col.key] }}</span>
          </template>
        </el-table-column>

      </template>

      <el-table-column
          show-overflow-tooltip="true"
          label="操作"
          align="center"
          width="200">
        <template #default="{row, index}">
          <div v-show="!row._edit">
            <el-button type="primary" @click="editElement(row)">编辑</el-button>
            <el-button type="danger" @click="deleted">删除</el-button>
          </div>
          <div v-show="row._edit">
            <el-button type="warning" @click="saveElement(row)">保存</el-button>
            <el-button type="info" @click="closeEditElement(row, index)">取消</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

  </el-card>
</template>

<script setup lang="ts" name="EditPage">
import {ElButton, ElMessage} from "element-plus";
import {h, onMounted, reactive, ref} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import {useUiElementApi} from "/@/api/useUiApi/uiElement";

const props = defineProps({
  pageId: {
    type: Number,
    default: 0
  }
})

const tableRef = ref()
const tagInputRef = ref()

const state = reactive({
  columns: [
    {
      key: 'name', label: '元素名称', width: '', show: true,
      render: (row: any) => h(ElButton, {
        link: true,
        type: "primary",
        onClick: () => {
          onOpenSaveOrUpdate("update", row)
        }
      }, () => row.name)
    },
    {key: 'location_type', label: '定位类型', width: '', align: 'center', show: true},
    {key: 'location_value', label: '定位值', width: '', align: 'center', show: true},
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
  ],
  elementList: [],
  total: 0,

  locationTypes: [
    {label: 'id', value: 'id'},
    {label: 'name', value: 'name'},
    {label: 'xpath', value: 'xpath'},
    {label: 'class_name', value: 'class_name'},
    {label: 'tag_name', value: 'tag_name'},
    {label: 'css_selector', value: 'css_selector'},
    {label: 'link_text', value: 'link_text'},
    {label: 'partial_link_text', value: 'partial_link_text'},
    {label: 'url', value: 'url'},
    {label: 'title', value: 'title'},
  ],

//   tmpElRows
  tmpElRows: {},
});

const getElementList = () => {
  tableRef.value.openLoading()
  useUiPageApi().getList(state.listQuery)
    .then((res: any) => {
      state.elementList = res.data.list;
      state.total = res.data.total;

    })
    .finally(() => {
      tableRef.value.closeLoading()
    })
};

// 编辑元素
const editElement = (row: any) => {
  state.tmpElRows[row.id] = {...row}
  row._edit = true
}

// 关闭编辑状态
const closeEditElement = (row: any, index: number) => {
  if (row.id) {
    row._edit = false
  } else {
    state.elementList.splice(index, 1)
  }
}
// 更新保存 元素
const saveElement = (row: any) => {
  // 判断有 row.page_name 则保存，不然就是url为空
  if (row.location_type && row.name) {
    useUiElementApi().saveOrUpdate(row)
      .then(res => {
        row._edit = false
        ElMessage.success('保存成功')
        // 保存成功后不刷新页面，直接塞入id， 不然后面点删除数据id为空
        row.id = res.data.id
      })
  } else {
    ElMessage.warning('元素，或者定位值不能为空!')
  }
}

const addElement = () => {
  state.elementList.push({
    name: '',
    location_type: '',
    location_value: '',
    page_id: '',
    remarks: '',
    _edit: true,
  })

}


onMounted(() => {
})
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