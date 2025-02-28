<template>
  <div>
    <div v-if="extractResultsData.length > 0">
      <el-table :data="extractResultsData">
        <el-table-column prop="name" label="变量名" show-overflow-tooltip=""></el-table-column>
        <el-table-column prop="extract_type" label="提取类型" show-overflow-tooltip=""></el-table-column>
        <el-table-column prop="extract_value" label="提取值" show-overflow-tooltip="">
          <template #default="{row}">
            {{ getJson2Str(row.extract_value) }}
          </template>
        </el-table-column>

        <el-table-column prop="extract_result" label="提取结果" show-overflow-tooltip="">
          <template #default="{ row }">
            <el-tag :type="row.extract_result === 'pass'? 'success': 'danger'">{{ row.extract_result }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="错误信息" show-overflow-tooltip=""></el-table-column>
      </el-table>
    </div>

    <div v-if="Object.keys(extractsData).length > 0">
      <el-divider>
        <el-icon>
          <ele-StarFilled/>
        </el-icon>
        提取数据
        <el-icon>
          <ele-StarFilled/>
        </el-icon>
      </el-divider>
      <JsonViews :data="extractsData"></JsonViews>
    </div>
  </div>
</template>

<script setup name="ReportExtracts">
import {computed} from 'vue';
import JsonViews from "/src/components/Z-JsonViews/index.vue";

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
  extractResults: {
    type: Array,
    default: () => {
      return []
    }
  }
})

const extractsData = computed(() => {
  return props.data
})

const extractResultsData = computed(() => {
  return props.extractResults
})

const getJson2Str = (value) => {
  try {
    return JSON.stringify(value)
  } catch (e) {
    return value
  }
}

</script>

<style lang="scss" scoped>

</style>