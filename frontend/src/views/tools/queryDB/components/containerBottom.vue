<template>
  <el-tabs
      v-model="activeName"
      type="card"
      class="demo-tabs"
      closable
      @tab-remove="removeTab"
  >
    <el-tab-pane
        v-for="item in data"
        :key="item.name"
        :label="item.title"
        :name="item.name"
        size="small"
    >
      <div style="overflow-y: auto">
        <el-table :data="findTableData(item.tabIndex)"
                  border
                  fit
                  size="small"
                  :max-height="tableHeight"
                  style="width: 100%">
          <el-table-column
              v-for="(value ,key) in  findTableData(item.tabIndex)[0]"
              :label="key"
              :prop="key"
              :key="key"
              align="center"
              :show-overflow-tooltip="true"
              width="auto"
          >
          </el-table-column>

        </el-table>
      </div>

    </el-tab-pane>
  </el-tabs>
</template>
<script lang="ts">
import {defineComponent, reactive, toRefs, getCurrentInstance, onMounted, onUnmounted} from 'vue';

export default defineComponent({

  name: 'app',
  setup() {
    const {proxy} = <any>getCurrentInstance();
    const state = reactive({
      activeName: 'test',
      tableHeight: 200,
      tabIndex: 0,
      data: []
    });

    // 根据对于的 tabIndex 获取对于tab数据
    const findTableData = (tabIndex: number) => {
      return state.data.find((e) => e.tabIndex == tabIndex).content
    }


    const addTab = (result: string) => {
      let tabIndex = ++state.tabIndex
      const newTabName = `结果${tabIndex}`
      state.data.push({
        title: newTabName,
        tabIndex: tabIndex,
        name: newTabName,
        content: result,
      })
      state.activeName = newTabName
      console.log(state.data, "state.data")
    }

    const removeTab = (targetName: string) => {
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

    const setTableHeight = (tableHeight: number) => {
      state.tableHeight = tableHeight - 60
    }

    onMounted(() => {
      //插入sql查询结果
      proxy.mittBus.on("setExecuteResult", (result: any) => {
        addTab(result)
      })

    })

    onUnmounted(() => {
      proxy.mittBus.off("setExecuteResult")
    })


    return {
      addTab,
      setTableHeight,
      findTableData,
      removeTab,
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>

:deep(.el-tabs__content) {
  overflow: auto;
}


</style>