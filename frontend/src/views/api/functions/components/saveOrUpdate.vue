<template>
  <div>
    <div style=" height: 45px" class="header">
      <el-form ref="formRef"
               v-model="funcFrom"
               inline
               label-width="auto"
      >
        <el-form-item prop="name" label="函数名称">
          <el-input type="primary"
                    size=""
                    placeholder="备注"
                    style="width: 200px"
                    v-model="funcFrom.name">
          </el-input>

          <el-button type="primary" @click="showDiff=!showDiff" style="margin-left: 10px;">保存</el-button>

        </el-form-item>

        <el-form-item>
        </el-form-item>

      </el-form>

    </div>

    <div class="code-box">
      <!--      展示-->
      <monaco-editor
          v-model:value="funcFrom.content"
          v-model:long="long"
      ></monaco-editor>
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
import {defineComponent, onMounted, reactive, toRefs} from "vue";
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
        name: ''
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
              state.funcFrom.name = res.data.name
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
            state.showDiff = false
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
.header {
  display: flex;
  padding: 10px 5px;
  background-color: #ffffff;
  border-radius: 0px;
  border-left: 5px solid #409eff;
}

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
