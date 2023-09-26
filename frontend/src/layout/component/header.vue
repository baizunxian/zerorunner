<template>
	<el-header class="layout-header" v-show="!isTagsViewCurrenFull">
		<NavBarsIndex />
	</el-header>
</template>

<script setup name="layoutHeader">
import {storeToRefs} from 'pinia';
import {useTagsViewRoutes} from '/@/stores/tagsViewRoutes';
import NavBarsIndex from '/@/layout/navBars/index.vue';

// 定义变量内容
const storesTagsViewRoutes = useTagsViewRoutes();
const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
</script>
