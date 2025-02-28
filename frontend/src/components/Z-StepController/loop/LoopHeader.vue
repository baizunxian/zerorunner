<template>
  <el-row>
    <el-col :span="20" class="com-padding">
      <el-radio-group v-model="data.request.loop_type" @click.stop>
        <el-radio label="count">次数循环</el-radio>
        <el-radio label="for">for循环</el-radio>
        <el-radio label="while">while循环</el-radio>
      </el-radio-group>
    </el-col>
  </el-row>
</template>

<script setup name="LoopHeader">
import {reactive} from 'vue';

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {
        // data: {
        //   name: '次数循环',
        //   loop_type: 'count',   // count 次数循环， for for循环， while while循环
        //   value: {
        //     count_number: 0,  // 循环次数
        //     count_interval_time: 0,  // 间隔时间
        //   },
        // }

        // data: {
        //   name: 'for循环',
        //   loop_type: 'for',   // number 次数循环， for for循环， while while循环
        //   value: {
        //     for_variable_name: "",  // 变量名
        //     for_variable: "",  // 变量
        //     for_interval_time: 0,  // 间隔时间 秒
        //   },
        // }

        // data: {
        //   name: 'While循环',
        //   loop_type: 'for',   // number 次数循环， for for循环， while while循环
        //   value: {
        //     while_variable: "",  // 变量
        //     while_comparator: "",  // 比对规则
        //     while_value: "",  // 比对值
        //     while_sleep_time: 3,  // 循环间隔时间 秒
        //     while_timeout: 3,  // 超时时间 秒
        //   },
        // }
      }
    }
  }
})

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
    none: "空",
    not_none: "非空",
  },
});

</script>

<style lang="scss" scoped>
.com-padding {
  padding: 0 3px;
}
</style>