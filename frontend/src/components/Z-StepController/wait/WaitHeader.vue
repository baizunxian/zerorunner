<template>
  <el-input-number v-model="data.request.wait_time"
                   controls-position="right"
                   @click.stop=""/>
  <span style="margin-left: 5px">s</span>
</template>

<script setup name="WaitHeader">

import useVModel from "/@/utils/useVModel";

const emit = defineEmits(['update:data'])
const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

const data = useVModel(props, 'data', emit)

</script>
