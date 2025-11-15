<template>
	<div class="response">
		<el-collapse v-model="state.accordionName">
			<el-collapse-item name="body">
				<template #title>
					<strong>Body</strong>
				</template>
				<z-monaco-editor style="height: 400px" ref="monacoEditRef" :options="{ readOnly: true }" v-model:value="result" lang="json"></z-monaco-editor>
			</el-collapse-item>
		</el-collapse>
	</div>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, watch } from 'vue';

defineOptions({ name: 'ResponseInfo' });

const props = defineProps({
	data: {
		type: Object,
		required: true,
	},
	stat: {
		type: Object,
		required: true,
	},
});

const result = computed(() => {
	let res = '';
	try {
		res = JSON.stringify(props.data.result, null, 4);
	} catch (e) {
		console.log(e);
	}
	return res;
});

const state = reactive({
	// show
	accordionName: ['body', 'header', 'cookies'],
	response: props.data,
	body: '',
	content_type: '',
});

const initData = () => {
	state.response = props.data;
};

watch(
	() => props.data,
	() => {
		nextTick(() => {
			initData();
		});
	},
	{ deep: true }
);

onMounted(() => {
	nextTick(() => {
		initData();
	});
});
</script>

<style lang="scss" scoped>
.response {
	.response-info {
		margin-bottom: 15px;

		.response-info__item {
			margin-right: 8px;
		}
	}
}
</style>
