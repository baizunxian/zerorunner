import {capitalize, defineComponent, h, markRaw} from 'vue';
import ResizeObserver from 'resize-observer-polyfill';
import ace from 'ace-builds';
import 'ace-builds/src-noconflict/ext-language_tools';
import 'ace-builds/src-noconflict/theme-monokai'
import 'ace-builds/src-noconflict/ext-searchbox';
import 'ace-builds/src-noconflict/mode-json';
import 'ace-builds/src-noconflict/mode-sql';
import 'ace-builds/src-noconflict/mode-text';
import 'ace-builds/src-noconflict/mode-python';
import workerPythonUrl from 'ace-builds/src-noconflict/mode-python.js?url';
import workerJsonUrl from 'ace-builds/src-noconflict/worker-json.js?url';
ace.config.setModuleUrl('ace/mode/python_worker', workerPythonUrl);
ace.config.setModuleUrl('ace/mode/json_worker', workerJsonUrl);
const Events = [
  'blur',
  'input',
  'change',
  'changeSelectionStyle',
  'changeSession',
  'copy',
  'focus',
  'paste',
];
export const VAceEditor = defineComponent({
  props: {
    value: {
      type: String,
      required: true,
    },
    lang: {
      type: String,
      default: 'text',
    },
    theme: {
      type: String,
      default: 'chrome',
    },
    options: Object,
    placeholder: String,
    readonly: Boolean,
    wrap: Boolean,
    printMargin: {
      type: [Boolean, Number],
      default: true,
    },
    minLines: Number,
    maxLines: Number,
  },
  emits: ['update:value', 'init', ...Events],
  render() {
    return h('div');
  },
  mounted() {
    this.ace = ace
    const editor = this._editor = markRaw(ace.edit(this.$el, {
      placeholder: this.placeholder,
      readOnly: this.readonly,
      value: this.value,
      mode: 'ace/mode/' + this.lang,
      theme: 'ace/theme/' + this.theme,
      wrap: this.wrap,
      printMargin: this.printMargin,
      useWorker: true,
      minLines: this.minLines,
      maxLines: this.maxLines,
      ...this.options,
    }));
    this.contentBackup = this.value;
    this.isSettingContent = false;
    editor.on('change', () => {
      if (this.isSettingContent)
        return;
      const content = editor.getValue();
      this.contentBackup = content;
      this.$emit('update:value', content);
    });
    Events.forEach(x => {
      const eventName = 'on' + capitalize(x);
      if (typeof this.$.vnode.props[eventName] === 'function') {
        editor.on(x, this.$emit.bind(this, x));
      }
    });
    this._ro = new ResizeObserver(() => editor.resize());
    this._ro.observe(this.$el);
    this.$emit('init', editor);
  },
  beforeUnmount() {
    var _a, _b;
    (_a = this._ro) === null || _a === void 0 ? void 0 : _a.disconnect();
    (_b = this._editor) === null || _b === void 0 ? void 0 : _b.destroy();
  },
  methods: {
    focus() {
      this._editor.focus();
    },
    blur() {
      this._editor.blur();
    },
    selectAll() {
      this._editor.selectAll();
    },
  },
  watch: {
    value(val) {
      if (this.contentBackup !== val) {
        try {
          this.isSettingContent = true;
          this._editor.setValue(val, 1);
        } finally {
          this.isSettingContent = false;
        }
        this.contentBackup = val;
      }
    },
    theme(val) {
      this._editor.setTheme('ace/theme/' + val);
    },
    options(val) {
      this._editor.setOptions(val);
    },
    readonly(val) {
      this._editor.setReadOnly(val);
    },
    placeholder(val) {
      this._editor.setOption('placeholder', val);
    },
    wrap(val) {
      this._editor.setWrapBehavioursEnabled(val);
    },
    printMargin(val) {
      this._editor.setOption('printMargin', val);
    },
    lang(val) {
      this._editor.setOption('mode', 'ace/mode/' + val);
    },
    minLines(val) {
      this._editor.setOption('minLines', val);
    },
    maxLines(val) {
      this._editor.setOption('maxLines', val);
    },
  }
});
