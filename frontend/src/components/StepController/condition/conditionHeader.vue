<template>
  <el-row @click.stop>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.check" placeholder="变量,例如：${var}"/>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-select size="small"
                 v-model="data.comparator"
                 placeholder=""
                 filterable
                 class="w100">
        <el-option
            v-for="(value, key) in comparatorOptions"
            :key="key"
            :label="value"
            :value="key">
        </el-option>

      </el-select>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.expect" placeholder="值"/>
    </el-col>
    <el-col :span="6" class="com-padding">
      <el-input v-model="data.remarks" placeholder="备注"/>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'conditionController',
  props: {
    data: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  emits: ['update:data'],
  setup() {
    const state = reactive({
      // data
      showDetail: false,
      comparatorOptions: {
        equals: "等于",
        not_equals: "不等于",
        contains: "包含",
        not_contains: "不包含",
        gt: "大于",
        lt: "小于",
        none: "空",
        not_none: "非空",
      },
    });
    // 删除节点
    return {
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
.com-padding {
  padding: 0 3px;
}
</style>