<template>
  <pre>
      {{data}}
    </pre>
</template>

<script lang="ts">
import {defineComponent} from 'vue';


export default defineComponent({
  name: 'scriptController',
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup(props: any) {

    // 删除节点
    return {

    };
  },
});
</script>

<style lang="scss" scoped>

</style>