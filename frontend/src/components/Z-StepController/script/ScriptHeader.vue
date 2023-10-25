<template>
  <el-collapse-transition>
    <div v-show="step.showDetail" @click.stop="" style="margin-top: 8px">
      <div style="border: 1px solid #E6E6E6; padding: 8px">
        <ScriptController v-model:codeContent="step.request.script_content"
                          use-type="case"></ScriptController>
      </div>
    </div>
  </el-collapse-transition>
</template>

<script setup name="ScriptHeader">
import useVModel from "/@/utils/useVModel";
import ScriptController from "/@/components/Z-StepController/script/ScriptController.vue";

const props = defineProps({
  step: {
    type: Object,
    required: true
  }

})

const emit = defineEmits(['update:step'])

const step = useVModel(props, 'step', emit)

</script>

<style lang="scss" scoped>


</style>