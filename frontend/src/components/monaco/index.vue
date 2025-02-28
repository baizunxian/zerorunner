<template>
  <div class="monaco-editor" ref="monacoEditorRef"></div>
</template>
<script setup name="monacoEditor">
import * as monaco from 'monaco-editor'
import {onMounted, onUnmounted, reactive, ref, toRaw, watch} from 'vue'
import SQLSnippets from "./core/sql.js"
import {getJsonPath} from '/@/utils/jsonPath'
import {ElMessage} from "element-plus";
import commonFunction from "/@/utils/commonFunction";

const props = defineProps({
  // 展示的字符串
  // modelValue: {
  //   type: String,
  //   default: '',
  // },
  value: {
    type: String,
    default: '',
  },
  // 是否启用比对
  isDiff: {
    type: Boolean,
    default: false,
  },
  readOnly: {
    type: Boolean,
    default: false,
  },
  // 比对需要的源数据
  oldString: {
    type: String,
    default: '',
  },
  // // 比对需要的新数据
  // newString: {
  //   type: String,
  //   default: '',
  // },
  // 语言
  lang: {
    type: String,
    default: 'python',
  },
  // 主题
  theme: {
    type: String,
    default: 'vs',   // vs ||  hc-black || vs-dark
  },
  //lineNumbers
  options: {
    type: Object,
    default: () => {
      return {}
    }
  },

  executeHandle: {
    type: Function,
  },

  dbList: {
    type: Array,
    default: () => []
  },
  onInputTableAlia: {
    type: [Array, Function],
    default: () => []
  },
  onInputField: {
    type: Array,
    default: () => []
  },
  dbs: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(["on-cursor-change", "update:value"])

const editor = ref(null)
const monacoEditorRef = ref()
const originalEditor = ref(null)
const modifiedEditor = ref(null)
const state = reactive({
  sqlSnippets: null,
  contentBackup: null,
  isSettingContent: false,
  jsonPath: null,
  options: {
    value: props.value,  // 值
    theme: props.theme,   // 主题
    autoIndex: true,  //
    language: props.lang, // 语言类型
    tabCompletion: 'on',
    cursorSmoothCaretAnimation: true,
    formatOnPaste: true,
    mouseWheelZoom: function (e) {
      const editor = e.target;
      const isAtBottom = editor.getScrollTop() >= editor.getScrollHeight() - editor.getLayoutInfo().height;
      if (isAtBottom) {
        e.browserEvent.stopPropagation(); // 阻止 Monaco Editor 捕获事件
      }
      return false; // 禁用默认的缩放行为
    },
    folding: true, //代码折叠
    autoClosingBrackets: 'always',
    autoClosingOvertype: 'always',
    autoClosingQuotes: 'always',
    automaticLayout: 'always',
  }
})

const initEditor = () => {
  // 初始化编辑器，确保dom已经渲染
  let options = {...state.options, ...props.options}
  state.sqlSnippets = new SQLSnippets(
      monaco,
      props.onInputField,
      props.onInputTableAlia,
      props.dbs
  )

  monaco.languages.register({id: props.lang})
  monaco.languages.registerCompletionItemProvider(
      props.lang,
      {
        async provideCompletionItems(model, position) {
          let suggestions = []
          switch (props.lang) {
            case "sql":
              return await state.sqlSnippets.provideCompletionItems(model, position)
            default:
              // language = pythonLanguage
              // language.keywords.forEach((item) => {
              //   suggestions.push({
              //     label: item,
              //     kind: monaco.languages.CompletionItemKind.Keyword,
              //     insertText: item
              //   });
              // })
              return {
                // suggestions: cloneDeep(vCompletion),//自定义代码补全
                suggestions: suggestions
              }
          }

        },
        triggerCharacters: ['.'],
      }
  )
  let modEditor
  if (props.isDiff) {
    editor.value = monaco.editor.createDiffEditor(monacoEditorRef.value, options)
    originalEditor.value = monaco.editor.createModel(props.value, props.lang)
    modifiedEditor.value = monaco.editor.createModel(props.oldString, props.lang)
    toRaw(editor.value).setModel({
      original: toRaw(originalEditor.value),
      modified: toRaw(modifiedEditor.value)
    })
    registerCustomEvent(editor.value.getModifiedEditor())
    registerCustomEvent(editor.value.getOriginalEditor())
    toRaw(editor.value.getModifiedEditor()).updateOptions({readOnly: props.readOnly});
    toRaw(editor.value.getOriginalEditor()).updateOptions({readOnly: props.readOnly});

    // setOptions()

  } else {
    editor.value = monaco.editor.create(monacoEditorRef.value, options)
    modEditor = editor.value
    registerCustomEvent(modEditor)
    modEditor.onDidChangeModelContent(() => {
      if (state.isSettingContent)
        return;
      const content = getValue();
      state.contentBackup = content;
      emit("update:value", content)

    })
  }
}

// 获取value
const getValue = () => {
  return toRaw(editor.value).getValue()
}

const setValue = (val) => {
  const isReadOnly = toRaw(editor.value).getRawOptions().readOnly;
  if (isReadOnly) {
    toRaw(editor.value).setValue(val)
  } else {
    const undoStack = getModel().undoStack;
    toRaw(editor.value).executeEdits("replaceText", [{
      range: getModel().getFullModelRange(),
      text: val,
      forceMoveMarkers: true
    }]);
    getModel().undoStack = undoStack;
  }
  setLineColor()
}

const getSelectionValue = () => {
  return toRaw(editor.value).getModel().getValueInRange(toRaw(editor.value).getSelection())
}

const getModel = () => {
  return toRaw(editor.value).getModel()
}

const foldAll = () => {
  toRaw(editor.value).getAction('editor.foldAll').run()
}

const unfoldAll = () => {
  toRaw(editor.value).getAction('editor.unfoldAll').run()
}

const registerCustomEvent = (editor) => {
  if (props.lang === 'json') {
    editor.addAction({
      id: 'json-path', // action unique id
      label: '复制 JsonPath', // action 在右键时展示的名称
      precondition: null,
      keybindingContext: "editorLangId == 'json'",
      contextMenuGroupId: 'navigation',// 右键展示位置
      // keybindings: [
      //   monaco.KeyMod.chord(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyJ)
      // ],

      run: copyToClipboard
    })
  }

  if (props.lang === 'sql') {
    editor.addAction({
      id: 'executeSql', // action unique id
      label: '执行', // action 在右键时展示的名称
      precondition: null,
      keybindingContext: "editorLangId == 'sql'",
      contextMenuGroupId: 'navigation',// 右键展示位置
      run: () => {
        if (props.executeHandle) props.executeHandle()
      }
    })

  }

  editor.onDidChangeCursorPosition((event) => {
    if (!props.isDiff) {
      let value = getValue()
      let offSet = toRaw(getModel()).getOffsetAt(event.position)
      let language = props.lang;

      if (props.value !== value && language === 'json') {
        emit('on-cursor-change', {offSet: offSet})
      }
      if (language === 'json' && offSet !== 0) {
        state.jsonPath = getJsonPath(value, offSet)
        // emit('on-jsonpath-change', {jsonPath: state.jsonPath})
      }
    }

  })

  editor.onMouseWheel((e) => {
    const scrollTop = editor.getScrollTop();
    const scrollHeight = editor.getScrollHeight();
    const clientHeight = editor.getLayoutInfo().height;
    // 获取鼠标滚轮事件信息
    const deltaY = e.deltaY; // 获取滚轮的垂直滚动方向
    if ((deltaY > 0 && scrollTop + clientHeight >= scrollHeight) || (deltaY < 0 && scrollTop === 0)) {
      // 如果触底或触顶，则执行外部容器的滚动事件
      // 可以模拟滚动或者执行其他滚动事件相关的操作
      // 阻止编辑器默认的滚轮事件，以防止冲突
      e.stopPropagation();
      // e.preventDefault()

    }
  });


}

const copyToClipboard = () => {
  if (state.jsonPath) {
    commonFunction().copyText(state.jsonPath, `复制成功 🎉  ${state.jsonPath}`)
  } else {
    ElMessage.warning("没有可复制的路径...");
  }
}


const setLineColor = () => {
  toRaw(editor.value).createDecorationsCollection([
    {
      options: {
        // className: 'monaco-content-class',
        isWholeLine: true,
        backgroundColor: '#FFA500'
      },
      // 装饰位置
      range: {
        startColumn: 1,
        endColumn: 30,
        startLineNumber: 1,
        endLineNumber: 2
      }
    }
  ])
}

const setOptions = (options = {}) => {
  toRaw(editor.value).updateOptions({
    // renderSideBySide: false,  // 并排显示
    ...props.options,
    ...options,
  });
}

watch(
    () => props.value,
    (newVal) => {
      if (state.contentBackup !== newVal) {
        try {
          state.isSettingContent = true;
          setValue(newVal)
        } finally {
          state.isSettingContent = false;
        }
        state.contentBackup = newVal;
      }

    },
    {deep: true}
)

watch(
    () => props.lang,
    (newVal) => {
      if (props.isDiff) {
        // toRaw(editor.value).getOriginalEditor().setModelLanguage(toRaw(editor.value).getOriginalEditor().getModel(), newVal)
        // toRaw(editor.value).getModifiedEditor().setModelLanguage(toRaw(editor.value).getModifiedEditor().getModel(), newVal)
      } else {
        monaco.editor.setModelLanguage(toRaw(editor.value).getModel(), newVal)
      }
    },
    {deep: true}
)
watch(
    () => props.theme,
    () => {
      monaco.editor.setTheme(props.theme)

    },
    {deep: true}
)
watch(
    () => props.isDiff,
    () => {
      toRaw(editor.value)?.dispose()
      initEditor()
    },
    {deep: true}
)
watch(
    () => props.oldString,
    (newVal) => {
      toRaw(originalEditor.value).setValue(newVal)
    },
    {deep: true}
)
// watch(
//     () => props.newString,
//     (newVal) => {
//       toRaw(modifiedEditor.value).setValue(newVal)
//     },
//     {deep: true}
// )

watch(
    () => props.dbs,
    () => {
      state.sqlSnippets.setDbSchema(props.dbs)
    },
    {deep: true}
)

onMounted(() => {
  initEditor()
})

onUnmounted(() => {
  toRaw(editor.value)?.dispose()
})


defineExpose({
  getValue,
  getModel,
  setValue,
  foldAll,
  unfoldAll,
  getSelectionValue,
})
</script>
<style>
.monaco-editor {
  width: 100%;
  height: 100%;
}

.monaco-content-class {
  background-color: #FFA500;
  opacity: 0.5;
}
</style>