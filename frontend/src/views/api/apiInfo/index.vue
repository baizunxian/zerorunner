<template>
  <el-tabs v-model="activeName" class="case-tabs">
    <el-tab-pane label="接口列表" name="case_list">
      <case-list></case-list>
    </el-tab-pane>
    <el-tab-pane label="接口树" name="case_tree">
      <case-tree></case-tree>
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';
import caseList from "/@/views/api/apiInfo/components/apiList.vue";
import caseTree from "/@/views/api/apiInfo/components/apiTree.vue";


export default defineComponent({
  name: 'apiInfo',
  components: {
    caseTree,
    caseList,
  },
  setup() {

    const state = reactive({
      activeName: "case_list",
    });

    return {

      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-tabs), .case-tabs {
  background-color: #FFFFFF;
  border-radius: 10px;
}

:deep(.el-tabs__header) {
  margin: 0;
  padding: 0 10px;
}
</style>