<template>
  <el-card>
    <z-table
        :columns="state.columns"
        :data="state.elementList"
        ref="tableRef"
        :border="false"
        v-model:page-size="state.listQuery.pageSize"
        v-model:page="state.listQuery.page"
        :total="state.total"
        @pagination-change="getElementList"
    >
    </z-table>
  </el-card>
</template>

<script setup name="UiElement">
import {ElButton, ElInput, ElMessage, ElMessageBox, ElOption, ElSelect} from "element-plus";
import {h, reactive, watch} from "vue";
import {useUiElementApi} from "/@/api/useUiApi/uiElement";
import {RefreshLeft, Edit, CirclePlus} from "@element-plus/icons"


const props = defineProps({
  pageId: {
    type: Number,
    default: 0
  }
})

const state = reactive({
  columns: [
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {
      key: 'name', label: '元素名称', width: '', align: 'center', show: true,
      render: ({row}) => h(ElInput, {
        modelValue: row.name,
        placeholder: '请输入元素名称',
        clearable: true,
      }),
    },
    {
      key: 'location_method', label: '定位方式', width: '', align: 'center', show: true,
      render: ({row}) => h(ElSelect, {
          style: 'width: 100%',
          modelValue: row.location_method,
          placeholder: '请选择定位方式',
          clearable: true,
        }, () => state.locationTypes.map((type) => h(ElOption, {
          key: type.value,
          label: type.label,
          value: type.value
        }))
      ),
      renderHeader: () => h('div', {}, [
        h('span', {
          style: 'margin-right: 10px'
        }, "定位方式"),
        h(ElButton, {
          type: "primary",
          icon: Edit,
          round: true,
        }, () => "编辑"),
        h(ElButton, {
          type: "success",
          icon: RefreshLeft,
          round: true,
        }, () => "刷新")
      ])
    },
    {
      key: 'location_value', label: '定位值', width: '', align: 'center', show: true,
      render: ({row}) => h(ElInput, {
        modelValue: row.location_value,
        placeholder: '请输入定位值',
        clearable: true,
      },)
    },
    {
      key: 'remarks', label: '备注', width: '', align: 'center', show: true,
      render: ({row}) => h(ElInput, {
        modelValue: row.remarks,
        placeholder: '请输入备注',
        clearable: true,
      },)
    },
    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      render: ({row, $index}) => h("div", null, [
        h(ElButton, {
          type: "primary",
          onClick: () => {
            saveElement(row)
          }
        }, () => '保存'),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deletedElement(row, $index)
          }
        }, () => '删除')
      ]),
      renderHeader: () => h('div', {}, [
        h(ElButton, {
          type: "success",
          icon: CirclePlus,
          round: true,
          onClick: () => {
            addElement()
          }
        }, () => "添加元素")
      ])
    },
  ],
  elementList: [],
  total: 0,
  loading: false,
  listQuery: {
    page: 1,
    pageSize: 10,
    page_id: null
  },

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

});

const getElementList = () => {
  state.loading = true
  useUiElementApi().getList(state.listQuery)
    .then((res) => {
      state.elementList = res.data.rows;
      state.total = res.data.rowTotal;
    })
    .finally(() => {
      state.loading = false
    })
};


const addElement = () => {
  state.elementList.unshift({
    page_id: props.pageId,
    name: '',
    location_method: '',
    location_value: '',
    remarks: '',
  })

}

// 更新保存 元素
const saveElement = (row) => {
  console.log(state, "state")
  // 判断有 row.page_name 则保存，不然就是url为空
  if (row.location_method && row.name) {
    useUiElementApi().saveOrUpdate(row)
      .then(res => {
        row._edit = false
        ElMessage.success('保存成功')
        // 保存成功后不刷新页面，直接塞入id， 不然后面点删除数据id为空
        if (!row.id) {
          state.total++
        }
        row.id = res.data.id
      })
  } else {
    ElMessage.warning('元素，或者定位值不能为空!')
  }
}


// 删除
const deletedElement = (row, index) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    if (!row.id) {
      state.elementList.splice(index, 1)
      return
    }
    useUiElementApi().deleted({id: row.id})
      .then((res) => {
        ElMessage.success('删除成功')
        getElementList()
      })
  })
}

watch(
  () => props.pageId,
  (page_id) => {
    state.elementList = []
    if (page_id) {
      state.listQuery.page_id = props.pageId
      getElementList()
    }
  },
  {
    deep: true,
  }
);

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

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

</style>