<template>
  <pre>{{ data }}</pre>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, watch} from 'vue';


export default defineComponent({
  name: 'log',
  props: {
    data: String
  },
  emits: ['update:data'],
  setup(props: any) {
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

    // 删除节点
    return {};
  },
});
</script>

<style lang="scss" scoped>

</style>