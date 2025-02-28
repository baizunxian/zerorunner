<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <z-detail-page-header
            class="page-header"
            style="margin: 5px 0;"
        >
        </z-detail-page-header>
      </template>
      <UiCaseInfo ref="UiCaseInfoRef"
                  :data="state.uiCaseData"
                  @save-ui-case="saveUiCase"
                  @debug-ui-case="debugUiCase"
      ></UiCaseInfo>
      <el-card>
        <template #header>
          <div style="display: flex">
              <div class="">
                <span>测试步骤：</span>
                <span>{{ state.uiStepDataList.length }}</span>
              </div>
<!--              <div class="">-->
<!--                <span>场景变量：</span>-->
<!--                <span>{{ state.uiStepDataList.length }}</span>-->
<!--              </div>-->
            </div>
        </template>
<!--        <div style="padding: 8px 0">-->
<!--          <el-card>-->
<!--            -->
<!--          </el-card>-->
<!--        </div>-->
        <UiStepInfo ref="UiCaseStepRef" :step-data-list="state.uiStepDataList"></UiStepInfo>
      </el-card>
    </el-card>

    <UiDebugPage :step-data-list="state.uiStepDataList" ref="uiDebugPageRef"></UiDebugPage>
  </div>
</template>

<script setup name="uiCase">
import {onMounted, reactive, ref} from "vue";
import {useUiCaseApi} from "/@/api/useUiApi/uiCase";
import {useRoute} from 'vue-router'
import UiCaseInfo from "./uiCaseInfo.vue";
import UiStepInfo from "./uiStepInfo.vue";
import {ElMessage} from "element-plus";
import UiDebugPage from "/@/views/ui/uiCase/uiDebugPage.vue";

const route = useRoute();
const UiCaseInfoRef = ref();
const UiCaseStepRef = ref();
const uiDebugPageRef = ref();

const props = defineProps({
  caseId: {
    type: [String, Number],
    default: ''
  }
})

const state = reactive({
  uiCaseData: [],
  uiStepDataList: []
});

const getCaseById = () => {
  let case_id = props.caseId || route.query.id
  if (case_id) {
    useUiCaseApi().getUiCaseById({id: case_id})
      .then((res) => {
        state.uiCaseData = res.data
        state.uiStepDataList = res.data.steps
        UiCaseInfoRef.value.setData(res.data)
        // UiCaseStepRef.value.setData(res.data.steps)
      })
  }
};

// 保存用例
const saveUiCase = () => {
  let caseInfoData = UiCaseInfoRef.value.getData()
  if (state.uiStepDataList.length === 0) {
    ElMessage.warning("请添加测试步骤！")
    return
  }
  let uiCaseForm = {
    ...caseInfoData,
    steps: state.uiStepDataList
  }
  useUiCaseApi().saveOrUpdate(uiCaseForm).then((res) => {
    // UiCaseInfoRef.value.setData(res.data)
    // UiCaseStepRef.value.setData(res.data.steps)
    ElMessage.success("保存成功！")
  })
}

// 调试用例
const debugUiCase = () => {
  uiDebugPageRef.value.onOpenDebugPage()
}

// 页面加载时
onMounted(() => {
  getCaseById();
});

</script>

<style scoped lang="scss">

</style>