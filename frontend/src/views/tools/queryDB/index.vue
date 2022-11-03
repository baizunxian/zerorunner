<template>
  <div>
    <el-card shadow="hover" style="height: 100%">
      <splitpanes class="default-theme" @resize="paneSize = $event[0].size" style="height: 100%;">
        <pane :size="32">
          <db-list></db-list>
        </pane>
        <pane :size="100">
          <splitpanes class=""
                      ref="containerRef"
                      @resize="winChange('resize', $event)"
                      @ready="winChange('ready', $event)"
                      :horizontal="true">
            <pane :size="50">
              <container-top ref="containerTopRef"></container-top>
            </pane>
            <pane :size="50">
              <container-bottom ref="containerBottomRef"></container-bottom>
            </pane>
          </splitpanes>
        </pane>
      </splitpanes>
    </el-card>
  </div>

</template>

<script lang="ts">
import {defineComponent, reactive, toRefs, ref} from 'vue';
import dbList from '/@/views/tools/queryDB/components/dbList.vue';
import containerTop from '/@/views/tools/queryDB/components/containerTop.vue';
import containerBottom from '/@/views/tools/queryDB/components/containerBottom.vue';
import {Splitpanes, Pane} from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';

export default defineComponent({
  name: 'query_db',
  components: {
    dbList,
    containerTop,
    containerBottom,
    Splitpanes,
    Pane,
  },
  setup() {
    const containerRef = ref()
    const containerTopRef = ref()
    const containerBottomRef = ref()
    const state = reactive({
      paneSize: 50,
    });

    const winChange = (changeType: string, $event: any) => {
      containerRef.value.$nextTick(() => {
        let topHeight = containerRef.value.$el.offsetHeight
        let BottomHeight = containerRef.value.$el.offsetHeight
        if (changeType == 'resize') {
          topHeight = containerRef.value.$el.offsetHeight * $event[0].size / 100
          BottomHeight = containerRef.value.$el.offsetHeight * $event[1].size / 100
        }
        containerTopRef.value.setMonacoHeHeight(topHeight)
        containerBottomRef.value.setTableHeight(BottomHeight)
      })
    }

    return {
      winChange,
      containerRef,
      containerTopRef,
      containerBottomRef,
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>

:deep(.el-card) {
  height: 100%;

  .el-card__body {
    height: 100%;
    padding: 5px;
  }
}

.splitpanes.default-theme .splitpanes__pane {
  background-color: #ffffff;
}

.splitpanes__pane .content {
  padding: 0 6px;
}

:deep(.el-tabs) {
  height: 100%;

  .el-tabs__header {
    //height: 30px;
  }
}
</style>