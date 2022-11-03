<template>
  <div class="echart-pie-wrap">
    <div class="myEditorTop">[{{ isEdit ? '编辑' : '只读' }}] - [{{ debugtalkfrom.project_name }}]
      <el-button v-show="isEdit" type="success" size="mini" @click="save" style="margin-left: 10px;">保存</el-button>
    </div>
    <editor
        width="100%"
        ref="editor"
        :content="debugtalkfrom.debug_talk"
        v-model="debugtalkfrom.debug_talk"
        :options="options"
        theme="monokai"
        lang="python"
        @init="editorInit">
    </editor>
  </div>
</template>
<script>
// import {saveDebugTalk, getDebugTalkInfo} from '@/api/apiCase'
import {mapGetters} from 'vuex'

export default {
  name: 'editDebugtalk',
  // components: {editor: require('vue2-ace-editor')},
  data() {
    return {
      isEdit: true,
      debugtalkfrom: {
        id: null,
        debug_talk: '',
        project_name: ''
      },
      find_content: null,
      options: {
        enableBasicAutocompletion: true, // 启用基本自动完成
        enableSnippets: true, // 启用代码段
        enableLiveAutocompletion: true, // 启用实时自动完成
        printMarginColumn: 30,
        displayIndentGuides: true, // 显示参考线
        enableEmmet: true, // 启用Emmet
        tabSize: 4, // 标签大小
        fontSize: 14, // 设置字号
        useWorker: true, // 使用辅助对象
        showPrintMargin: false, //去除编辑器里的竖线
        enableMultiselect: true, //     选中多处
        readOnly: false, // 是否只读
        showFoldWidgets: true, // 显示折叠部件
        fadeFoldWidgets: true, // 淡入折叠部件
        wrap: true, //换行
        animatedScroll: true,
      }
    }
  },
  computed: {
    ...mapGetters([
      'userId'
    ])
  },

  watch: {
    debugtalkfrom: {
      handler(val) {
        console.log('this.find_content', this.find_content)
        this.goto(this.find_content)
      },
      deep: true
    },
  },

  beforeRouteEnter(to, form, next) {
    next((vm) => {
      vm.resetform()
      vm.find_content = to.query.find_content
      if (to.query.find_content) vm.goto(to.query.find_content)
    })
  },
  methods: {
    editorInit() {
      // require('brace/ext/language_tools')
      // require('brace/ext/searchbox')
      // require('brace/mode/python')
      // require('brace/snippets/python')
      // require('brace/theme/monokai')
    },
    //重置表单
    async resetform() {
      let form = {
        id: null,
        common: null
      }
      if (this.$route.query.type === 'common') {
        form.common = 'common'
      } else {
        form.id = this.$route.query.id
      }
      try {
        let res = await getDebugTalkInfo(form)
        if (res) {
          this.debugtalkfrom.id = res.data.id
          this.debugtalkfrom.debug_talk = res.data.debug_talk ? res.data.debug_talk : ''
          this.debugtalkfrom.project_name = res.data.project_name
          this.isEdit = res.data.edit
        }
      } catch (err) {
        this.$message.error(err)
      }
    },

    // 保存套件
    save() {
      saveDebugTalk(this.debugtalkfrom)
          .then(res => {
            if (res.msg === 'OK') {
              this.$message({
                type: 'success',
                message: '保存成功！'
              })
            }
          })
    },
    goto(fund_content) {
      if (this.find_content) {
        this.$nextTick(() => {
          this.$refs.editor.editor.find(`def ${fund_content}(`)
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.echart-pie-wrap {
  width: 100%;
  height: calc(100% - 45px);

  .myEditorTop {
    height: 45px;
    display: flex;
    align-items: center;
    background-color: #333;
    padding-left: 50px;
    color: rgb(241, 238, 8);
    font-weight: bold;
  }
}
</style>