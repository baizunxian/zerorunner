<template>
  <el-table
      :data="listData"
      :size="size"
      ref="ZTableRef"
      class="z-table"
      :tree-props="treeProps"
      :row-key="rowKey || ''"
      v-bind="attrs"
      :load="load"
      :border="border"
      v-loading="tableLoading"
      row-class-name="d-row-class-name"
      :lazy="lazy"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
      @cell-click="handleCellClick"
      @sort-change="handleSortChange">
    <el-table-column width="40" align="center" v-if="sortable">
      <template #default="">
        <div class="move" style="cursor: all-scroll">
          <el-icon class="step-rank">
            <Rank></Rank>
          </el-icon>
        </div>
      </template>
    </el-table-column>

    <template v-for="(col, index) in columns">

      <!---复选框, 序号 (START)-->
      <el-table-column
          :key="index"
          class-name="index-class"
          v-if="col.columnType === 'index' || col.columnType === 'selection' || col.columnType === 'expand'"
          :sortable="col.sortable"
          :render-header="col.renderHeader"
          v-bind="col"
          :prop="col.key"
          :fixed="col.fixed"
          :align="col.align"
          :label="col.label"
          :type="col.columnType"
          :index="indexMethod"
          :width="col.width">

        <template #default="scope">
          <component v-if="col.render"
                     :is="col.render"
                     :row="scope.row"
                     :index="scope.$index"
                     v-bind="scope"/>
        </template>
      </el-table-column>
      <!---复选框, 序号 (END)-->
      <!---图片 (START)-->
      <el-table-column
          v-else
          :key="index + 1"
          v-bind="col"
          :render-header="col.renderHeader"
          :show-overflow-tooltip="col.show"
          :sortable="col.sortable"
          :type="col.columnType"
          :prop="col.key"
          :align="col.align"
          :fixed="col.fixed"
          :label="col.label"
          :width="col.width">
        <!-- 自定义表头 -->
        <template #header="{ column, $index }">
          <component v-if="col.headerRender" :is="col.headerRender" :column="column" :index="$index"/>
          <slot v-else-if="col.headerSlot" :name="col.headerSlot" :column="column" :index="$index"></slot>
          <span v-else>{{ col.label }}</span>
        </template>

        <template #default="scope">
          <!-- 如需更改图片size，可自行配置参数 -->
          <el-image
              v-if="col.columnType === 'image'"
              preview-teleported
              :hide-on-click-modal="true"
              :preview-src-list="[scope.row[col.prop]]"
              :src="scope.row[col.prop]"
              fit="cover"
              style="width:40px;height:40px;border-radius:8px"/>

          <!-- 如果传递按钮数组，就展示按钮组 START-->
          <el-button-group v-else-if="col.buttons?.length">
            <el-button
                v-for="(btn, index) in col.buttons"
                size="small"
                :key="index"
                :type="btn.type"
                @click="handleAction(btn.command, scope)"
            >{{ btn.name }}
            </el-button>
          </el-button-group>
          <!-- 如果传递按钮数组，就展示按钮组 END-->

          <!--- 格式化日期 (本项目日期是时间戳，这里日期格式化可根据你的项目来更改) (START)-->
          <el-button-group v-else-if="col.columnType === 'date'">
            <span>{{ (scope.row[col.prop]).format(col.dateFormat ?? 'YYYY-MM-DD') }}</span>
          </el-button-group>
          <!--- 格式化日期 (本项目日期是时间戳，这里日期格式化可根据你的项目来更改) (END)-->
          <!-- render函数 (START) 使用内置的component组件可以支持h函数渲染和txs语法-->
          <component v-else-if="col.render"
                     :is="col.render"
                     v-model.lazy="scope.row[col.key]"
                     :row="scope.row"
                     :index="scope.$index"
                     v-bind="scope"/>
          <!-- render函数 (END) -->
          <!-- 自定义slot (START) -->
          <slot v-else-if="col.slot" :name="col.slot" :row="scope.row" :index="scope.$index"></slot>
          <!-- 自定义slot (END) -->
          <!-- 默认渲染 (START) -->
          <span v-else>{{ handleRow(scope.row, col.key, col.lookupCode) }}</span>
          <!-- 默认渲染 (END) -->

        </template>
      </el-table-column>
    </template>
  </el-table>
  <!-- 分页器 -->
  <div v-show="showPage" class="mt20">
    <el-pagination
        small
        :total="total"
        :page-size="pageSize"
        :layout="layout"
        :current-page="page"
        @size-change="pageSizeChange"
        @current-change="currentPageChange"/>
  </div>
</template>
<script setup name="z-table">
import {computed, nextTick, onMounted, reactive, ref} from 'vue'
import {useAttrs} from "vue";
import {formatLookup} from '/@/utils/lookup'
import Sortable from "sortablejs";
import {Rank} from "@element-plus/icons";
import useVModel from "/@/utils/useVModel";

const ZTableRef = ref()
const attrs = useAttrs()

const emit = defineEmits([
  "update:data",
  "update:pageSize",
  "update:page",
  "update:loading",
  "pagination-change",
  "current-change",
  "command",
  "selection-change",
  "row-click",
  "cell-click",
  "sort-change",
])
const props = defineProps({
  // 列表
  data: {
    type: Array,
    default: () => []
  },
  // table的数据
  columns: {
    type: Array,
    default: () => []
  },
  // 每列的配置项
  options: {
    type: Object,
    default: () => {
      return {
        stripe: false,
        border: true,
        tooltipEffect: 'dark',
        showHeader: true,
        showPagination: true,
        // rowStyle: () => 'cursor:pointer' // 行样式
      }
    }
  },
  rowKey: {
    type: String,
    default() {
      return undefined
    }
  },
  border: {
    type: Boolean,
    default() {
      return true
    }
  },
  // treeProps
  treeProps: {
    type: Object,
    default() {
      return {}
    }
  },
  // 分页
  showPage: {
    type: Boolean,
    default: () => true
  },
  // 远程加载
  lazy: {
    type: Boolean,
    default: () => {
      return false
    }
  },
  // 加载回调函数
  load: {
    type: Function,
    default: () => {
    }
  },
  // 加载回调函数
  size: {
    type: String,
    default: () => {
      return "small"
    }
  },
  // 是否显示占位符
  showPlaceholder: {
    type: Boolean,
    default: () => {
      return false
    }
  },
  placeholder: {
    type: String,
    default: () => {
      return "-"
    }
  },
  // 页数
  page: {
    type: Number,
    default: 0
  },
  // 页面大小
  pageSize: {
    type: Number,
    default: 10
  },
  // 总数
  total: {
    type: Number,
    default: 0
  },
  //
  pageSizes: {
    type: Array,
    default() {
      return [10, 20, 30, 50, 100, 200]
    }
  },
  layout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  loading: {
    type: Boolean,
    default: () => {
      return false
    }
  },
  sortable: {
    type: Boolean,
    default: () => {
      return false
    }
  },

})

const getRowKey = (row) => {
  if (props.rowKey) {
    return props.rowKey
  }
  // if (row) {
  //   if (!row._secondId) {
  //     row._secondId = Math.random() + ''
  //   }
  //   return row._secondId
  // } else {
  //   return Math.random() + ''
  // }
}


const listData = useVModel(props, 'data', emit)
// const listData = computed({
//   get: () => {
//     return props.data.constructor === Array ? props.data : []
//   },
//   set: (val) => {
//     emit('update:data', val)
//   }
// })

const state = reactive({
  tableLoading: false,
})

const tableLoading = computed(() => {
  return props.loading || state.tableLoading
})


const createSortable = () => {
  if (!props.sortable) return
  const el = ZTableRef.value.$el.querySelector('.z-table .el-table__body-wrapper tbody')
  if (el) {
    Sortable.create(el, {
      animation: 200,
      sort: true,
      handle: ".move",
      fallbackClass: "custom-fallback-class",
      forceFallback: true,
      onEnd: ({newIndex, oldIndex}) => {
        let newStepData = listData.value
        const currRow = newStepData.splice(oldIndex, 1)[0]
        newStepData.splice(newIndex, 0, currRow)
        nextTick(() => {
          listData.value = [...newStepData]
        })
      }
    });
  }
}


// 自定义索引
const indexMethod = (index) => {
  if (!props.showPage) return index + 1
  return index + (props.page - 1) * props.pageSize + 1
}
// 切换pageSize
const pageSizeChange = (pageSize) => {
  emit('update:pageSize', pageSize)
  emit('pagination-change', {page: props.page, limit: pageSize})
}
// 切换currentPage
const currentPageChange = (currentPage) => {
  emit('current-change', currentPage)
  emit('update:page', currentPage)
  emit('pagination-change', {page: currentPage, limit: props.pageSize})
}
// 按钮组事件
const handleAction = (command, scope) => {
  emit('command', command, scope.row)
}
// 多选事件
const handleSelectionChange = (val) => {
  emit('selection-change', val)
}
// 当某一行被点击时会触发该事件
const handleRowClick = (row, column, event) => {
  emit('row-click', row, column, event)
}
// 当某个单元格被点击时会触发该事件
const handleCellClick = (row, column, cell, event) => {
  emit('cell-click', row, column, cell, event)
}
// 当表格的排序条件发生变化的时候会触发该事件
// 在列中设置 sortable 属性即可实现以该列为基准的排序， 接受一个 Boolean，默认为 false。 可以通过 Table 的 default-sort 属性设置默认的排序列和排序顺序。 如果需要后端排序，需将 sortable 设置为 custom，同时在 Table 上监听 sort-change 事件， 在事件回调中可以获取当前排序的字段名和排序顺序，从而向接口请求排序后的表格数据。
const handleSortChange = ({column, prop, order}) => {
  emit('sort-change', {column, prop, order})
}

const handleRow = (row, key, lookupCode) => {
  if (props.showPlaceholder && (!row[key] || row[key] === '' || row[key] === null)) {
    return props.placeholder
  } else {
    return lookupCode ? formatLookup(lookupCode, row[key]) : row[key]
  }
}

const openLoading = () => {
  if (props.loading) {
    emit('update:loading', true)
  } else {
    state.tableLoading = true
  }
}

const closeLoading = () => {
  if (props.loading) {
    emit('update:loading', false)
  } else {
    state.tableLoading = false
  }
}

onMounted(() => {
  nextTick(() => {
    createSortable()
  })
})

defineExpose({
  openLoading,
  closeLoading
})


</script>
<style lang="scss" scoped>
:deep(.el-image__inner) {
  transition: all 0.3s;
  cursor: pointer;

  &:hover {
    transform: scale(1.2);
  }
}

.d-row-class-name {
  max-height: 23px;
}

:deep(.el-table__placeholder) {
  display: none;
}

</style>

