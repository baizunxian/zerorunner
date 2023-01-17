<template>
  <div>
    <el-card style="height: 100%">
      <z-splitpanes class="default-theme" @resize="paneSize = $event[0].size" style="height: 100%;">
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
            </pane>
          </z-splitpanes>
        </pane>
      </z-splitpanes>
    </el-card>
  </div>

</template>

<script lang="ts">
import {defineComponent, reactive, toRefs, ref} from 'vue';
import dbList from '/@/views/tools/queryDB/components/dbList.vue';
import containerTop from '/@/views/tools/queryDB/components/containerTop.vue';
import containerBottom from '/@/views/tools/queryDB/components/containerBottom.vue';

export default defineComponent({
  name: 'query_db',
  components: {
    dbList,
    containerTop,
    containerBottom,
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

</style>