<template>
  <div>
    <div style=" height: 45px">[{{ isEdit ? '编辑' : '只读' }}] - [{{ funcFrom.project_name }}]
      <el-button v-show="isEdit" type="success" @click="saveOrUpdate" style="margin-left: 10px;">保存</el-button>
    </div>
    <el-button type="success" @click="showDiff=!showDiff" style="margin-left: 10px;">showDiff
    </el-button>


    <div class="code-box">
      <!--      展示-->
      <monaco-editor
          v-model:value="funcFrom.content"
          v-model:long="long"
      />
    </div>


    <el-dialog
        v-if="showDiff"
        v-model="showDiff"
        title="比对"
        top="5vh"
        width="80%"
        :destroy-on-close="true"

    >
      <template #header>
        <div style="display: flex">
          <span style="font-size: 16px; font-weight: 600; padding-right: 20px">函数比对</span>
          <el-button type="primary" @click="saveOrUpdate">确认保存</el-button>
        </div>
      </template>
      <div class="diff-box">
        <el-row class="diff-box__title">
          <el-col :span="12">修改前</el-col>
          <el-col :span="12">修改后</el-col>
        </el-row>

        <monaco-editor
            :isDiff="true"
            v-model:oldString="originalFuncContent"
            v-model:value="funcFrom.content"
            v-model:long="long"
        />
      </div>

    </el-dialog>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from "vue";
import {useRoute} from 'vue-router'
import {useFunctionsApi} from "/@/api/useAutoApi/functions";
import {ElMessage} from "element-plus/es";

export default defineComponent({
  name: 'saveOrUpdateDebugTalk',
  setup() {
    const route = useRoute()
    const state = reactive({
      isEdit: true,
      editor: null,
      originalFuncContent: "",
      funcFrom: {
        id: null,
        content: '',
        project_name: ''
      },

      long: 'python',

      // diff
      showDiff: false,

    });

    const initData = () => {
      if (route.query) {
        useFunctionsApi().getFuncInfo(route.query)
            .then(res => {
              state.funcFrom.content = res.data.content
              state.originalFuncContent = res.data.content
              state.funcFrom.project_name = res.data.project_name
              state.funcFrom.id = res.data.id
              state.isEdit = res.data.edit
              // initEditor(state.debugTalkFrom.debug_talk)
            })
      }
    }
    // 新增
    const saveOrUpdate = () => {
      useFunctionsApi().saveOrUpdate(state.funcFrom)
          .then(() => {
            ElMessage.success('操作成功');
          })
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };

    // diff

    onMounted(() => {
      initData()
    })

    return {
      initData,
      saveOrUpdate,
      ...toRefs(state),
    };
  },
})

</script>

<style lang="scss" scoped>
.echart-pie-wrap {
  //height: calc(100% - 45px);

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

.code-box {
  height: calc(100% - 45px);
}

.diff-box {
  height: 75vh;

  .diff-box__title {
    //text-align: center;
  }
}
</style>
