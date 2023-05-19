<template>
  <el-table
      :data="data"
      :tree-props="treeProps"
      :row-key="rowKey"
      v-bind="options"
      :load="load"
      :border="border"
      v-loading="tableLoading"
      row-class-name="d-row-class-name"
      :lazy="lazy"
      @selection-change="handleSelectionChange"
      @row-click="handleRowClick"
      @cell-click="handleCellClick"
      @sort-change="handleSortChange">
    <template v-for="(col, index) in columns" :key="index">
      <!---复选框, 序号 (START)-->
      <el-table-column
          class-name="index-class"
          v-if="col.columnType === 'index' || col.columnType === 'selection' || col.columnType === 'expand'"
          :sortable="col.sortable"
          :prop="col.key"
          :fixed="col.fixed"
          :align="col.align"
          :label="col.label"
          :type="col.columnType"
          :index="indexMethod"
          :width="col.width"/>
      <!---复选框, 序号 (END)-->
      <!---图片 (START)-->
      <el-table-column
          v-else-if="col.columnType === 'image'"
          :sortable="col.sortable"
          :prop="col.key"
          :align="col.align"
          :fixed="col.fixed"
          :label="col.label"
          :width="col.width">
        <template #default="{ row }">
          <!-- 如需更改图片size，可自行配置参数 -->
          <el-image
              preview-teleported
              :hide-on-click-modal="true"
              :preview-src-list="[row[col.prop]]"
              :src="row[col.prop]"
              fit="cover"
              style="width:40px;height:40px;border-radius:8px"/>
        </template>
      </el-table-column>
      <!---图片 (END)-->

      <!--- 日期格式化 (START)-->
      <el-table-column
          v-else-if="col.columnType === 'date'"
          :sortable="col.sortable"
          :prop="col.key"
          :align="col.align"
          :fixed="col.fixed"
          :label="col.label"
          :width="col.width">
        <template #default="{ row }">
          <span>{{ (row[col.prop]).format(col.dateFormat ?? 'YYYY-MM-DD') }}</span>
        </template>
      </el-table-column>
      <!---日期格式化 (END)-->
      <!-- 自定义slot (START) -->
      <el-table-column
          :show-overflow-tooltip="col.show"
          v-else-if="col.slot"
          :sortable="col.sortable"
          :prop="col.key"
          :align="col.align"
          :fixed="col.fixed"
          :label="col.label"
          :width="col.width">
        <template #default="scope">
          <slot :name="col.slot" :row="scope.row" :index="scope.$index"></slot>
        </template>
      </el-table-column>
      <!-- 自定义slot (END) -->

      <!-- 如果传递按钮数组，就展示按钮组 START-->
      <el-table-column
          v-else-if="col.buttons?.length"
          :align="col.align"
          :label="col.label"
          :fixed="col.fixed"
          :width="col.width">
        <template #default="scope">
          <el-button-group>
            <el-button
                v-for="(btn, index) in col.buttons"
                size="small"
                :key="index"
                :type="btn.type"
                @click="handleAction(btn.command, scope)"
            >{{ btn.name }}
            </el-button
            >
          </el-button-group>
        </template>
      </el-table-column>
      <!-- 如果传递按钮数组，就展示按钮组 END-->

      <!-- render函数 (START) -->
      <el-table-column
          :show-overflow-tooltip="col.show"
          v-else-if="col.render"
          :label="col.label"
          :sortable="col.sortable"
          :prop="col.key"
          :fixed="col.fixed"
          :align="col.align"
          :width="col.width">
        <template #default="scope">
          <!-- Expand组件代码下方有贴出来 -->
          <Expand :render="col.render"
                  :row="scope.row"
                  :index="scope.$index"/>
        </template>
      </el-table-column>
      <!-- render函数 (END) -->

      <!-- 默认渲染列 (START) -->
      <el-table-column
          :show-overflow-tooltip="col.show"
          v-else
          :label="col.label"
          :sortable="col.sortable"
          :prop="col.key"
          :fixed="col.fixed"
          :align="col.align"
          :width="col.width">
        <template #default="{row}">
          {{ handleRow(row, col.key, col.lookupCode) }}
        </template>
      </el-table-column>

      <!-- 默认渲染列 (END) -->
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
<script setup lang="ts" name="z-table">
import {computed, defineAsyncComponent, reactive} from 'vue'
import {formatLookup} from '/@/utils/lookup'

const Expand = defineAsyncComponent(() => import("./expand.vue"))

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
      return ""
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
  }
})

const state = reactive({
  tableLoading: false,
})

const tableLoading = computed(() => {
  return props.loading || state.tableLoading
})

const emit = defineEmits([
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


// 自定义索引
const indexMethod = (index: number) => {
  if (!props.showPage) return index + 1
  return index + (props.page - 1) * props.pageSize + 1
}
// 切换pageSize
const pageSizeChange = (pageSize: number) => {
  emit('update:pageSize', pageSize)
  emit('pagination-change', {page: props.page, limit: pageSize})
}
// 切换currentPage
const currentPageChange = (currentPage: number) => {
  emit('current-change', currentPage)
  emit('update:page', currentPage)
  emit('pagination-change', {page: currentPage, limit: props.pageSize})
}
// 按钮组事件
const handleAction = (command: any, scope: any) => {
  emit('command', command, scope.row)
}
// 多选事件
const handleSelectionChange = (val: any) => {
  emit('selection-change', val)
}
// 当某一行被点击时会触发该事件
const handleRowClick = (row: any, column: any, event: Event) => {
  emit('row-click', row, column, event)
}
// 当某个单元格被点击时会触发该事件
const handleCellClick = (row: any, column: any, cell: any, event: Event) => {
  emit('cell-click', row, column, cell, event)
}
// 当表格的排序条件发生变化的时候会触发该事件
// 在列中设置 sortable 属性即可实现以该列为基准的排序， 接受一个 Boolean，默认为 false。 可以通过 Table 的 default-sort 属性设置默认的排序列和排序顺序。 如果需要后端排序，需将 sortable 设置为 custom，同时在 Table 上监听 sort-change 事件， 在事件回调中可以获取当前排序的字段名和排序顺序，从而向接口请求排序后的表格数据。
const handleSortChange = ({column, prop, order}: any) => {
  emit('sort-change', {column, prop, order})
}

const handleRow = (row: any, key: string, lookupCode: string) => {
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

