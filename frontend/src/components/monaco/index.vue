<template>
  <div class="monaco-editor" ref="monacoEditorRef"></div>
</template>
<script lang="ts">
import * as monaco from 'monaco-editor'
import {reactive, ref, watch, onMounted, toRefs, toRaw} from 'vue'
import {language as pythonLanguage} from 'monaco-editor/esm/vs/basic-languages/python/python.js';

import SQLSnippets from "./core/sql.js"

export default {
  name: 'monaco-editor',
  props: {
    // 展示的字符串
    value: {
      type: String,
      default: '',
    },
    // 是否启用比对
    isDiff: {
      type: Boolean,
      default: false,
    },
    // 比对需要的源数据
    oldString: {
      type: String,
      default: '',
    },
    // 比对需要的新数据
    newString: {
      type: String,
      default: '',
    },
    // 语言
    long: {
      type: String,
      default: 'python',
    },
    // 主题
    theme: {
      type: String,
      default: 'vs-dark',   // vs hc-black  vs-dark
    },
    //lineNumbers
    options: {
      type: Object,
      default: () => {
        return {}
      }
    },

    dbList: {
      type: Array,
      default: () => []
    },
    onInputTableAlia: {
      type: Array,
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
  },
  emits: ["update:value"],
  setup(props: any, {emit}) {
    const monacoEditorRef = ref()
    const editor: any = ref(null)
    const originalEditor: any = ref(null)
    const modifiedEditor: any = ref(null)
    const state = reactive({
      sqlSnippets: null,
      contentBackup: null,
      isSettingContent: false,
      options: {
        value: props.value,  // 值
        theme: props.theme,   // 主题
        autoIndex: true,  //
        language: props.long, // 语言类型
        tabCompletion: 'on',
        cursorSmoothCaretAnimation: true,
        formatOnPaste: true,
        mouseWheelZoom: true,
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

      monaco.languages.register({id: props.long})
      monaco.languages.registerCompletionItemProvider(
          props.long,
          {
            async provideCompletionItems(model, position) {
              let suggestions: any = []
              let language: any = pythonLanguage
              switch (props.long) {
                case "sql":
                  return await state.sqlSnippets.provideCompletionItems(model, position)
                default:
                  language = pythonLanguage
                  language.keywords.forEach((item: any) => {
                    suggestions.push({
                      label: item,
                      kind: monaco.languages.CompletionItemKind.Keyword,
                      insertText: item
                    });
                  })
                  return {
                    // suggestions: cloneDeep(vCompletion),//自定义代码补全
                    suggestions: suggestions
                  }
              }

            },
            triggerCharacters: ['.'],
          }
      )
      let modEditor: any
      if (props.isDiff) {
        editor.value = monaco.editor.createDiffEditor(monacoEditorRef.value, options)
        originalEditor.value = monaco.editor.createModel(props.oldString, props.long)
        modifiedEditor.value = monaco.editor.createModel(props.value, props.long)
        toRaw(editor.value).setModel({
          original: toRaw(originalEditor.value),
          modified: toRaw(modifiedEditor.value)
        })

        modEditor = editor.value.getModifiedEditor()

      } else {
        editor.value = monaco.editor.create(monacoEditorRef.value, options)
        modEditor = editor.value
      }

      modEditor.onDidChangeModelContent((val: any) => {
        if (state.isSettingContent)
          return;
        const content = toRaw(modEditor).getValue();
        state.contentBackup = content;
        emit("update:value", content)
      })
      state.contentBackup = props.value;
      state.isSettingContent = false;
    }

    // 获取value
    const getValue = () => {
      return toRaw(editor.value).getValue()
    }

    const getMode = () => {
      return toRaw(editor.value).getModel()
    }


    watch(
        () => props.value,
        (newVal) => {
          if (state.contentBackup !== newVal) {
            try {
              state.isSettingContent = true;
              toRaw(editor.value).setValue(newVal)
            } finally {
              state.isSettingContent = false;
            }
            state.contentBackup = newVal;
          }

        },
        {deep: true}
    )

    watch(
        () => props.long,
        (newVal) => {
          monaco.editor.setModelLanguage(toRaw(editor.value).getModel(), newVal)
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
        () => props.oldString,
        (newVal) => {
          toRaw(originalEditor.value).setValue(newVal)
        },
        {deep: true}
    )
    watch(
        () => props.newString,
        (newVal) => {
          toRaw(modifiedEditor.value).setValue(newVal)
        },
        {deep: true}
    )

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

    return {
      getValue,
      getMode,
      initEditor,
      monacoEditorRef,
      ...toRefs(state)
    }
  }
}

</script>
<style scoped>
.monaco-editor {
  width: 100%;
  height: 100%;
}
</style>