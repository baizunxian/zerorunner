<template>
  <el-input-number v-model="data.value" @click.stop=""/>
  <span style="margin-left: 5px">m</span>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'waitHeader',
  props: {
    data: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  emits: ['update:data'],
  setup() {
    return {};
  },
});
</script>

<style lang="scss" scoped>

</style>