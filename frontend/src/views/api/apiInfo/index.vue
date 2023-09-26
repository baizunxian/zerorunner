<template>
  <div>

    <ApiList></ApiList>

    <!--  <el-card>-->
    <!--    <el-tabs v-model="activeName" class="apiInfo-tabs h100">-->
    <!--      <el-tab-pane label="接口列表" name="case_list">-->
    <!--        <apiInfo-list></apiInfo-list>-->
    <!--      </el-tab-pane>-->
    <!--      <el-tab-pane label="接口树" name="case_tree">-->
    <!--        <apiInfo-tree></apiInfo-tree>-->
    <!--      </el-tab-pane>-->
    <!--    </el-tabs>-->
    <!--  </el-card>-->
  </div>
</template>

<script setup name="apiInfo">
import {reactive} from 'vue';
import ApiList from "./components/ApiList.vue"

const state = reactive({
  activeName: "case_list",
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