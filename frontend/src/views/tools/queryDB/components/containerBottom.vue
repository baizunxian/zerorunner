<template>
  <el-tabs
      v-show="state.data.length > 0"
      v-model="state.activeName"
      type="card"
      class="demo-tabs"
      closable
      @tab-remove="removeTab"
  >
    <el-tab-pane
        v-for="item in state.data"
        :key="item.name"
        :label="item.title"
        :name="item.name"
        size="small"

    >
      <div style="overflow-y: auto">
        <el-table :data="findTableData(item.tabIndex)"
                  border
                  class="nowrap-tab w100"
                  size="small"
                  :max-height="state.tableHeight">
          <el-table-column
              v-for="(value ,key) in  findTableData(item.tabIndex)[0]"
              :label="key"
              :prop="key"
              :key="key"
              align="center"
              :render-header="renderHeader"
              :show-overflow-tooltip="true"
              width="auto"
          >
          </el-table-column>
        </el-table>
      </div>

    </el-tab-pane>
  </el-tabs>
</template>
<script setup name="containerBottom">
import {getCurrentInstance, h, nextTick, onMounted, onUnmounted, reactive} from 'vue';
import mittBus from '/@/utils/mitt';
import commonFunction from '/@/utils/commonFunction'

const {copyText} = commonFunction()


const {proxy} = getCurrentInstance();
const state = reactive({
  activeName: 'test',
  tableHeight: 200,
  tabIndex: 0,
  data: []
});

// 根据对于的 tabIndex 获取对于tab数据
const findTableData = (tabIndex) => {
  return state.data.find((e) => e.tabIndex == tabIndex).content
}


const addTab = (result) => {
  let tabIndex = ++state.tabIndex
  const newTabName = `结果${tabIndex}`
  state.data.push({
    title: newTabName,
    tabIndex: tabIndex,
    name: newTabName,
    content: result,
  })
  state.activeName = newTabName
}

const removeTab = (targetName) => {
  const tabs = state.data
  let activeName = state.activeName
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }

  state.activeName = activeName
  state.data = tabs.filter((tab) => tab.name !== targetName)
}

const setTableHeight = (tableHeight) => {
  nextTick(() => {
    state.tableHeight = tableHeight - 60
  })
}

const renderHeader = ({column, $index}) => {
  // 新建一个 span
  let span = document.createElement('span');
  // 设置表头名称
  span.innerText = column.label;
  // 临时插入 document
  document.body.appendChild(span);
  // 重点：获取 span 最小宽度，设置当前列，注意这里加了 20，字段较多时还是有挤压，且渲染后的 div 内左右 padding 都是 10，所以 +20 。（可能还有边距/边框等值，需要根据实际情况加上）
  column.minWidth = span.getBoundingClientRect().width + 20;
  // 移除 document 中临时的 span
  document.body.removeChild(span);
  return h('span', {
    style: {color: "#606266"},
    onClick: () => {
      copyText(column.label)
    }
  }, column.label);
}

onMounted(() => {
  //插入sql查询结果
  mittBus.on("setExecuteResult", (result) => {
    addTab(result)
  })

})

onUnmounted(() => {
  mittBus.off("setExecuteResult", () => {
  })
})

defineExpose({
  setTableHeight,
})

</script>

<style lang="scss" scoped>

:deep(.el-tabs__content) {
  overflow: auto;
}

</style>