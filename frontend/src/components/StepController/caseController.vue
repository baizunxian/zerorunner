<template>
  <el-collapse-transition>
    <div v-show="data.showDetail" @click.stop="">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <div style="border: 1px solid #E6E6E6">
        <case-info :case_id="data.value"></case-info>
      </div>
    </div>
  </el-collapse-transition>
</template>

<script lang="ts">
import {defineAsyncComponent, defineComponent, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'scriptController',
  components: {
    caseInfo: defineAsyncComponent(() => import("/@/views/api/apiCase/components/saveOrUpdate.vue"))
  },
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
    const state = reactive({
      // data
      showDetail: false
    });
    // 删除节点
    return {
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

</style>