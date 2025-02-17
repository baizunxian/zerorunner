<template>
  <div class="app-container h100">
    <el-card class="h100" :body-style="state.bodyStyle">
      <z-splitpanes class="default-theme" @resize="state.paneSize = $event[0].size" style="height: 100%;">
        <z-pane :size="32">
          <db-list></db-list>
        </z-pane>
        <z-pane :size="100">
          <z-splitpanes class=""
                        ref="containerRef"
                        @resize="winChange('resize', $event)"
                        @ready="winChange('ready', $event)"
                        :horizontal="true">
            <z-pane :size="50">
              <container-top ref="containerTopRef"></container-top>
            </z-pane>
            <z-pane :size="50">
              <container-bottom ref="containerBottomRef"></container-bottom>
            </z-pane>
          </z-splitpanes>
        </z-pane>
      </z-splitpanes>
    </el-card>
  </div>

</template>

<script setup name="QueryDB">
import {reactive, ref} from 'vue';
import dbList from '/@/views/tools/queryDB/components/dbList.vue';
import containerTop from '/@/views/tools/queryDB/components/containerTop.vue';
import containerBottom from '/@/views/tools/queryDB/components/containerBottom.vue';

const containerRef = ref()
const containerTopRef = ref()
const containerBottomRef = ref()
const state = reactive({
  paneSize: 50,
  bodyStyle: {height: "100%"}
});

const winChange = (changeType, $event) => {
  containerRef.value.$nextTick(() => {
    let topHeight = containerRef.value.$el.offsetHeight
    let BottomHeight = containerRef.value.$el.offsetHeight
    if (changeType === 'resize') {
      topHeight = containerRef.value.$el.offsetHeight * $event[0].size / 100
      BottomHeight = containerRef.value.$el.offsetHeight * $event[1].size / 100
    } else {
      topHeight = topHeight / 2
      BottomHeight = BottomHeight / 2
    }
    containerTopRef.value.setMonacoHeHeight(topHeight)
    containerBottomRef.value.setTableHeight(BottomHeight)
  })
}
</script>

<style lang="scss" scoped>


</style>