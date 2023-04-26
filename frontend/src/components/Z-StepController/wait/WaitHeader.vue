<template>
  <el-input-number v-model="data.wait_request.wait_time"
                   controls-position="right"
                   @click.stop=""/>
  <span style="margin-left: 5px">m</span>
</template>

<script lang="ts" setup name="WaitHeader">

import {PropType} from "vue";

const props = defineProps({
  data: {
    type: Object as PropType<TStepDataStat>,
    default: () => {
      return {}
    }
  },
})

</script>
