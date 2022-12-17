<template>
  <json-view v-model:data="data"></json-view>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, toRefs, watch} from 'vue';
import jsonView from "/@/components/jsonView/index.vue";


export default defineComponent({
  name: 'extracts',
  components: {jsonView},
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup(props: any) {
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

    return {
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>

</style>