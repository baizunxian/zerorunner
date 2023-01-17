<template>
  <el-input-number v-model="data.value"
                   @click.stop=""/>
  <span style="margin-left: 5px">m</span>
</template>

<script lang="ts" setup name="WaitHeader">

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

</script>
