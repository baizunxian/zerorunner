<template>
  <el-row @click.stop>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.request.check" placeholder="变量,例如：${var}"/>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-select size="small"
                 v-model="data.request.comparator"
                 placeholder=""
                 filterable
                 class="w100">
        <el-option
            v-for="(value, key) in state.comparatorOptions"
            :key="key"
            :label="value"
            :value="key">
        </el-option>

      </el-select>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.request.expect" placeholder="值"/>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.request.remarks" placeholder="备注"/>
    </el-col>
  </el-row>
</template>

<script setup name="IfStep">
import {reactive} from 'vue';
import useVModel from "/@/utils/useVModel";

const emit = defineEmits(["update:data"])

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

const data = useVModel(props, 'data', emit)

const state = reactive({
  // data
  showDetail: false,
  comparatorOptions: {
    equals: "等于",
    not_equal: "不等于",
    contains: "包含",
    not_contains: "不包含",
    gt: "大于",
    lt: "小于",
    is_none: "空",
    not_none: "非空",
  },
});

</script>

<style lang="scss" scoped>
.com-padding {
  padding: 0 3px;
}
</style>