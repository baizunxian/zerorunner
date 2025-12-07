<template>
  <div class="request">
    <h4>执行脚本</h4>
    <z-monaco-editor
        style="height: 82vh"
        ref="monacoEditRef"
        :options="{readOnly: true}"
        :value="ScriptContent"
        lang="python"
    ></z-monaco-editor>
  </div>
</template>

<script setup>
import {computed} from 'vue';

defineOptions({name: "ScriptRequestInfo"})

const props = defineProps({
  data: {
    type: Object,
    required: true,
  }
})
const ScriptContent = computed(() => {
  return props.data?.script_content || ""
})

</script>

<style lang="scss" scoped>
.request-info {
  margin-bottom: 15px;
}
</style>