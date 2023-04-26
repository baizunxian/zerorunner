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

<script lang="ts" setup name="DetailPageHeader">
import {reactive} from 'vue';

const emit = defineEmits(['back'])

const state = reactive({});

const back = () => {
  emit("back")
}

</script>

<style lang="scss" scoped>
:deep(.el-page-header__breadcrumb) {
  display: none;
}

</style>