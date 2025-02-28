<template>
  <pre>{{ data }}</pre>
</template>

<script setup name="ReportLog">
import {nextTick, onMounted, reactive, watch} from 'vue';

const props = defineProps({
  data: {
    type: String
  }
})

const state = reactive({
  // data
  log: props.data

});
watch(
    () => props.data,
    () => {
      state.log = props.data
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    state.log = props.data
  })
})


</script>
