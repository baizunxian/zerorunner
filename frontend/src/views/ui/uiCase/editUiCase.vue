<template>
  <div class="app-container">
    <el-button @click="addUiStep">测试</el-button>
    <UICaseStep ref="UiCaseStepRef" :data="state.uiCaseData"></UICaseStep>
  </div>
</template>

<script setup lang="ts" name="uiCase">
import {ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive, ref} from "vue";
import {useUiCaseApi} from "/@/api/useUiApi/uiCase";
import {useRouter, useRoute} from 'vue-router'
import UICaseStep from "/@/components/Z-UiStepController/index.vue";

const router = useRouter();
const route = useRoute();
const UiCaseStepRef = ref();

const props = defineProps({
  caseId: {
    type: [String, Number],
    default: ''
  }
})

const state = reactive({
  uiCaseData: [],
});

const getCaseById = () => {
  let case_id = props.caseId || route.query.case_id
  if (case_id) {
    useUiCaseApi().getCaseById({id: case_id})
      .then((res: any) => {
        state.uiCaseData = res.data
      })
  }
};

// 新增或修改
const onOpenSaveOrUpdate = (editType: string, row: any) => {
  let query: any = {}
  query.editType = editType
  if (row) query.id = row.id
  router.push({name: 'EditPage', query: query})
};


const addUiStep = () => {
  UiCaseStepRef.value.addData()
}

// 页面加载时
onMounted(() => {
  getCaseById();
});

</script>

<style scoped lang="scss">

</style>