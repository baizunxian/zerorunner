<template>
  <JsonViews :data="data"></JsonViews>
</template>

<script setup name="ReportExtracts">
import {nextTick, onMounted, reactive, watch} from 'vue';
import JsonViews from "/@/components/Z-JsonViews/index.vue";

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
  extractsData: props.data

});

watch(
    () => props.data,
    () => {
      state.extractsData = props.data
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    state.extractsData = props.data
  })
})

</script>

<style lang="scss" scoped>

</style>