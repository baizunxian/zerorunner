<template>
  <div>
    <el-page-header
        class="page-header"
        style="margin: 5px 0;"
        @back="back"
    >
      <template #content>
        <slot name="content"></slot>
      </template>
      <template #extra>
        <slot name="extra"></slot>
      </template>

    </el-page-header>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'detailPageHeader',
  components: {},
  setup(props: any, {emit}) {
    const state = reactive({});

    const back = () => {
      emit("back")
    }

    onMounted(() => {
    })

    return {
      back,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-page-header__breadcrumb) {
  display: none;
}

</style>