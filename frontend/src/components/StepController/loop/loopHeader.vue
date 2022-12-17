<template>
  <el-row>
    <el-col :span="20" class="com-padding">
      <el-radio-group v-model="data.loop_type" @click.stop>
        <el-radio label="count">次数循环</el-radio>
        <el-radio label="for">for循环</el-radio>
        <el-radio label="while">while循环</el-radio>
      </el-radio-group>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'loopHeader',
  props: {
    data: {
      type: Object,
      default: () => {
        return {
          // data: {
          //   name: '次数循环',
          //   loop_type: 'number',   // number 次数循环， for for循环， while while循环
          //   value: {
          //     run_number: 0,  // 循环次数
          //     interval_time: 0,  // 间隔时间
          //   },
          // }

          // data: {
          //   name: 'for循环',
          //   loop_type: 'for',   // number 次数循环， for for循环， while while循环
          //   value: {
          //     variable_name: "",  // 变量名
          //     variable: "",  // 变量
          //     interval_time: 0,  // 间隔时间 秒
          //   },
          // }

          // data: {
          //   name: 'While循环',
          //   loop_type: 'for',   // number 次数循环， for for循环， while while循环
          //   value: {
          //     variable: "",  // 变量
          //     comparator: "",  // 比对规则
          //     value: "",  // 比对值
          //     timeout: 3,  // 超时时间 秒
          //   },
          // }
        }
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