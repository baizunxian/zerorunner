<template>
  <el-input-number v-model="data.wait_request.wait_time"
                   controls-position="right"
                   @click.stop=""/>
  <span style="margin-left: 5px">m</span>
</template>

<script setup name="WaitHeader">

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

</script>
