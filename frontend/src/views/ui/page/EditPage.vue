<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <z-detail-page-header
            class="page-header"
            style="margin: 5px 0;"
            :edit-type="route.query.editType"
            @back="initPage"
        >
        </z-detail-page-header>
      </template>

      <UiPageInfo v-model:data="state.pageData"></UiPageInfo>
      <UiElement :page-id="state.pageData.id"></UiElement>
    </el-card>

  </div>
</template>

<script setup name="EditPage">
import {onMounted, reactive} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import UiPageInfo from "/@/views/ui/page/uiPageInfo.vue";
import UiElement from "/@/views/ui/page/uiElement.vue";
import {useRoute} from "vue-router";

const route = useRoute()

const state = reactive({
//
  pageData: {},
});

const initPage = async () => {
  if (route.query.id) {
    let {data} = await useUiPageApi().getPageById({id: route.query.id})
    state.pageData = data
  }
}

onMounted(() => {
  initPage()
})

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

</style>