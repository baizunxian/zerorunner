<template>
  <el-row>
    <el-col :span="24" class="com-padding">
      <div style="display: flex">
        <span style="margin: 0px 8px 0px 4px;font-size: 14px;"
              :style="{color: getMethodColor(data.request.method)}"
        >{{ data.request.method }}</span>
        <div>{{ data.request.name }}</div>
      </div>
    </el-col>
  </el-row>
</template>

<script setup name="LoopHeader">
import {PropType, reactive} from 'vue';
import {getMethodColor} from "/@/utils/case";

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
  showDetail: false,
});

</script>

<style lang="scss" scoped>
.com-padding {
  padding: 0 3px;
}
</style>