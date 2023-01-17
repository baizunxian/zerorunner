<template>
  <el-table :data="state.validateData.validate_extractor">
    <el-table-column prop="check" label="断言名称"></el-table-column>
    <!--    <el-table-column prop="expect" label="期望"></el-table-column>-->
    <el-table-column prop="expect_value" label="期望值"></el-table-column>
    <el-table-column prop="check_value" label="结果值"></el-table-column>
    <el-table-column prop="check_result" label="断言结果">
      <template #default="{ row }">
        <el-tag :type="row.check_result === 'pass'? 'success': 'danger'">{{ row.check_result }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="message" label="错误信息"></el-table-column>
  </el-table>
</template>

<script lang="ts" setup name="ReportValidators">
import {nextTick, onMounted, PropType, reactive, watch} from 'vue';


const props = defineProps({
  data: {
    type: Object as PropType<ValidateExtractor>,
    default: () => {
      return {}
    }
  },
},)

const state = reactive({
  // data
  validateData: props.data

});

const validatorsResult = () => {
  let result = 'pass'
  let validate_extractor = props.data.validate_extractor
  if (validate_extractor && validate_extractor.length > 0) {
    for (let i = 0; i < validate_extractor.length; i++) {
      if (validate_extractor[i].check_result === 'fail' && result === 'pass') result = 'fail'
    }
  } else {
    result = ""
  }

  return result
}


watch(
    () => props.data,
    () => {
      state.validateData = props.data
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    state.validateData = props.data
  })
})

defineExpose({
  validatorsResult,
})
</script>

<style lang="scss" scoped>

</style>