<template>
  <el-row>
    <el-col :span="8">
      <div>环境变量</div>
      <JsonViews v-if="state.envVariables" v-model:data="state.envVariables" :deep="1"></JsonViews>
    </el-col>
    <el-col :span="8">
      <div>用例变量</div>
      <JsonViews v-if="state.caseVariables" v-model:data="state.caseVariables" :deep="1"></JsonViews>
    </el-col>
    <el-col :span="8">
      <div>步骤变量</div>
      <JsonViews v-if="state.variables" v-model:data="state.variables" :deep="1"></JsonViews>
    </el-col>
  </el-row>
</template>

<script setup name="ReportVariables">
import {nextTick, onMounted, reactive, watch} from 'vue';
import JsonViews from "/src/components/Z-JsonViews/index.vue";

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  }
})

const state = reactive({
  // data
  variables: {},
  globalVariables: {},
  envVariables: {},
  caseVariables: {},
});

const initData = () => {
  state.variables = props.data.variables
  state.caseVariables = props.data.caseVariables
  state.globalVariables = props.data.variables
  state.envVariables = props.data.envVariables
}

onMounted(() => {
  nextTick(() => {
    initData()
  })
})

watch(
    () => props.data,
    () => {
      initData()
    },
    {deep: true}
)

</script>

<style lang="scss" scoped>

</style>