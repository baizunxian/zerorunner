<template>
  <el-collapse-transition>
    <div v-if="data.showDetail" @click.stop class="controller-content">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <ApiInfo isViews :api_id="data.case_id"></ApiInfo>
    </div>
  </el-collapse-transition>
</template>

<script setup name="apiInfoController">
import {defineAsyncComponent} from 'vue';

const ApiInfo = defineAsyncComponent(()=> import("/@/views/api/apiInfo/components/EditApi.vue"))

const props = defineProps({
  data: {
    type: Object,
    default: () => {
        return {}
      }
  },
  offsetWidth: Number
})

</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}

:deep(.el-card__body) {
  padding: 20px !important;
}

</style>