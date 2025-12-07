<template>
  <div class="response">

    <el-collapse v-model="state.accordionName">
      <el-collapse-item name="body">
        <template #title>
          <strong>Body</strong>
        </template>
        <z-monaco-editor
            style="min-height: 400px"
            ref="monacoEditRef"
            :options="{readOnly: true}"
            v-model:value="state.result"
            lang="json"
        ></z-monaco-editor>
      </el-collapse-item>
    </el-collapse>


  </div>
</template>

<script setup>
import {nextTick, onMounted, reactive, ref, watch} from 'vue';

const emit = defineEmits(['json-path-to-validator'])

defineOptions({name: "ResponseInfo"})

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  stat: {
    type: Object,
    required: true
  }
})


const state = reactive({
  // show
  accordionName: ['body', 'header', "cookies"],
  response: props.data,
  result: null,
  content_type: '',
});

const initData = () => {
  state.response = props.data
  state.content_type = state.response.content_type
  state.result = state.response.result
  try {
    state.result = JSON.stringify(state.result, null, 4)
  } catch (e) {
    console.log(e)
  }
}

const monacoEditRef = ref()
const init_monaco_action = () => {
  if (monacoEditRef.value) {
    const editor = monacoEditRef.value.monacoEditor
    editor.addAction({
      id: 'json-path-to-validator', // action unique id
      label: '添加JsonPath到断言', // action 在右键时展示的名称
      precondition: null,
      keybindingContext: "editorLangId == 'json'",
      contextMenuGroupId: 'navigation',// 右键展示位置
      // keybindings: [
      //   monaco.KeyMod.chord(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyJ)
      // ],
      run: () => {
        const jsonPath = monacoEditRef.value.state.jsonPath
        const value = monacoEditRef.value.state.currValue
        emit('json-path-to-validator', {jsonPath, value})
      }
    })
  }

}

watch(
    () => monacoEditRef.value?.monacoEditor,
    () => {
      nextTick(() => {
        setTimeout(() => {
          init_monaco_action()
        }, 10)
      })
    },
    // {deep: true}
)


watch(
    () => props.data,
    () => {
      nextTick(() => {
        initData()
      })
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    initData()
  })
})

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