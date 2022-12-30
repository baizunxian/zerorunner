<template>
  <el-collapse-transition>
    <div v-show="data.showDetail" @click.stop class="controller-content">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <case-info :case_id="data.case_id"></case-info>
    </div>
  </el-collapse-transition>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';
import caseInfo from "/@/views/api/apiInfo/components/saveOrUpdate.vue"

export default defineComponent({
  name: 'scriptController',
  components: {
    caseInfo,
  },
  props: {
    data: {
      type: Object,
      default: () => {
        return {}
      }
    },
    offsetWidth: Number
  },
  emits: ['update:data'],
  setup() {
    const state = reactive({});

    return {
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}

</style>