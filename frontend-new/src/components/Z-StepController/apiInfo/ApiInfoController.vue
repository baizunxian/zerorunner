<template>
  <el-collapse-transition>
    <div v-if="data.showDetail" @click.stop class="controller-content">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <ApiInfo :isView="true" :case_id="data.request.api_id"></ApiInfo>
    </div>
  </el-collapse-transition>
</template>

<script lang="ts" setup name="apiInfoController">
import {defineAsyncComponent, PropType} from 'vue';

const ApiInfo = defineAsyncComponent(()=> import("/@/views/api/apiInfo/components/EditApi.vue"))

const props = defineProps({
  data: {
    type: Object as PropType<TStepDataStat>,
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