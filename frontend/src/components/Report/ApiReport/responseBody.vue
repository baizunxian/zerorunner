<template>
  <div style="height: 200px">
    <monaco-editor
        v-model:value="responseBody"
        :long="'json'"
    >
    </monaco-editor>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import MonacoEditor from "/@/components/monaco/index.vue";


export default defineComponent({
  name: 'scriptController',
  components: {MonacoEditor},
  props: {
    data: Object
  },
  setup(props: any) {
    const responseBody = computed(() => {
      try {
        return JSON.stringify(props.data.body)
      } catch (e) {
        return props.data.body
      }
    });


    // 删除节点
    return {
      responseBody,
    };
  },
});
</script>

<style lang="scss" scoped>

</style>