<template>
  <el-row>
    <el-col :span="8">
      <div>环境变量</div>
      <JsonViews v-if="state.envVariables" v-model:data="state.envVariables"></JsonViews>
    </el-col>
    <el-col :span="8">
      <div>用例变量</div>
      <JsonViews v-if="state.variables" v-model:data="state.variables"></JsonViews>
    </el-col>
    <el-col :span="8">
      <div>会话变量</div>
      <JsonViews v-if="state.sessionVariables" v-model:data="state.sessionVariables"></JsonViews>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup name="ReportVariables">
import {nextTick, onMounted, reactive, watch} from 'vue';
import JsonViews from "/@/components/Z-JsonViews/index.vue";

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
  sessionVariables: {}
});

const initData = () => {
  state.variables = props.data.variables
  state.globalVariables = props.data.variables
  state.envVariables = props.data.envVariables
  state.sessionVariables = props.data.sessionVariables
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