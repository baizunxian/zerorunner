<template>
  <div>
    <el-row>
      <el-col :span="20">
        <div style="border: 1px solid #e6e6e6">
          <z-monaco-editor
              style="height: 500px"
              ref="monacoEditRef"
              v-model:value="scriptContent"
              :options="{ minimap: { enabled: false } }"
          />
        </div>
      </el-col>

      <el-col :span="4">
        <div style="padding: 8px">
          <div>代码片段</div>
          <div v-for="menu in sideMenu" :key="menu.label">
            <el-button type="primary" link @click="handlerCode(menu)">{{ menu.label }}</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts" name="ScriptController">
import {computed, nextTick, reactive, ref, watch} from 'vue';
import {stepTypeEnum} from '/@/utils/case';
// import { RegisterMonacoProvider, } from '/src/components/MonacoEditor/provider/RegisterProvider';
// import { EditorLangType } from '/src/components/MonacoEditor/index.d';


const emit = defineEmits(['update:stepData']);

const props = defineProps({
  useType: {
    type: String,
    default: () => {
      return 'setup';
    },
  },
  stepData: {
    type: Object,
    required: true,
  },
  variableList: {
    type: Array,
    default: () => [],
  },
});
const monacoEditRef = ref();

const scriptContent = ref('');

const stepData = computed({
  get() {
    return scriptContent.value;
  },
  set(val) {
    scriptContent.value = val;
  },
});

const setData = (val) => {
  scriptContent.value = val?.script_content || '';
};


const getData = () => {
  return {script_content: scriptContent.value}
};

const getDataLength = () => {
  return stepData.value?.length;
};

const state = reactive({
  content: stepData.value,
  setupMenu: [
    {label: '获取请求头', content: "zero.request.headers.get('key')"},
    {label: '获取环境变量', content: "zero.environment.get('key')"},
    {label: '获取变量', content: "zero.variables.get('key')"},
    {label: '设置请求头', content: "zero.request.headers.set('key', 'value')"},
    {label: '设置环境变量', content: "zero.environment.set('key', 'value')"},
    {label: '设置变量', content: "zero.variables.set('key', 'value')"},
    {label: '打印日志', content: "logger.info('logger')"},
  ],
  teardownMenu: [
    // {label: "获取请求头", content: "zero.headers.get('key')"},
    // {label: "获取环境变量", content: "zero.environment.get('key')"},
    {label: '获取变量', content: "zero.variables.get('key')"},
    // {label: "设置请求头", content: "zero.request.headers.set('key', 'value')"},
    // {label: "设置环境变量", content: "zero.environment.set('key', 'value')"},
    {label: '设置变量', content: "zero.variables.set('key', 'value')"},
    {label: '打印日志', content: "logger.info('logger')"},
  ],
  caseMenu: [
    {label: '添加请求', content: "res = requests.post('https://zerorunner.cn/api/list').json()"},
    {label: '打印日志', content: "logger.info('logger')"},
  ],
});

const sideMenu = computed(() => {
  switch (props.useType) {
    case 'setup':
    case 'script':
      return state.setupMenu;
    case 'teardown':
      return state.teardownMenu;
    case 'case':
      return state.caseMenu;
    default:
      return [];
  }
});

// 处理code
const handlerCode = (row: any) => {
  stepData.value = stepData.value
      ? stepData.value + `\n${row.content}`
      : row.content;
};

// const initMonacoProvider = () => {
//   nextTick(() => {
//     RegisterMonacoProvider([EditorLangType.Text, EditorLangType.Python], props.variableList, monacoEditRef.value?.monacoEditor)
//   });
// };


defineExpose({
  getDataLength,
  getData,
  setData
});
</script>

<style lang="scss" scoped></style>