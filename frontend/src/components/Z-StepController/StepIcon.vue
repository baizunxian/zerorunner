<script setup lang="ts">
import { stepTypeList } from "/@/utils/case";
import { computed } from "vue";

const { stepType } = defineProps({
  stepType: {
    type: String,
    default: ""
  },
  size: {
    type: String,
    default: "28px"
  },
  showBackground: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: ""
  }
})

const stepTypeInfo = computed(() => {
  return stepTypeList.find(item => item.value === stepType)
})

</script>


<template>
  <div class="step-icon"
       :title="stepTypeInfo?.label"
       :style="{background: showBackground ? stepTypeInfo?.background : 'transparent'}">
    <component v-if="stepTypeInfo?.icon"
               :style="{color: color ? color :stepTypeInfo.color, '--step-icon-size': size}"
               :is="stepTypeInfo.icon">
    </component>
  </div>
</template>

<style scoped lang="scss">

.step-icon {
  border-radius: 999px;
  //width: 32px;
  //height: 32px;
  //line-height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;

  :deep(i) {
    font-size: 20px;
    font-size: calc(var(--step-icon-size));
  }

  :deep(svg) {
    width: 20px;
    width: var(--step-icon-size);
    height: 20px;
    height: var(--step-icon-size);
  }

}

</style>