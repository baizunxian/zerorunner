<template>
  <div>
    <el-page-header
        class="page-header"
        style="margin: 5px 0;"
        @back="back"
    >
      <template #content>
        <span style="padding-right: 10px;" v-if="!slots.content">{{ content }}</span>
        <slot name="content" v-else></slot>
      </template>
      <template #extra>
        <slot name="extra"></slot>
      </template>

    </el-page-header>

  </div>
</template>

<script setup name="DetailPageHeader">
import {computed, useSlots} from 'vue';
import {useRoute, useRouter} from 'vue-router'

const route = useRoute()
const router = useRouter()
const slots = useSlots()
const props = defineProps({
  editType: String
})

const content = computed(() => {
  let editType = props.editType || route.query.editType
  if (!editType) return ""
  if (editType === 'save') return '新增'
  if (editType === 'update') return '更新'
  else return ""
})
const back = () => {
  router.go(-1)
  // console.log("back", emit)
  // emit("back")
}

</script>

<style lang="scss" scoped>
:deep(.el-page-header__breadcrumb) {
  display: none;
}

</style>