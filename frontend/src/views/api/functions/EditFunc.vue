<template>
  <div class="h100 app-container" style="position: absolute">
    <el-card class="h100" :body-style="{height:'calc(100% - 67.5px)'}">
      <template #header>
        <z-detail-page-header
            @back="goBack"
        >
          <template #content>
            <el-input type="primary"
                      size=""
                      placeholder="函数名称"
                      style="width: 200px; padding-right: 10px"
                      v-model="state.funcFrom.name">
            </el-input>
            <el-input type="primary"
                      size=""
                      placeholder="备注"
                      style="width: 200px"
                      v-model="state.funcFrom.remarks">
            </el-input>

            <el-button type="primary" @click="showDiffPage" style="margin-left: 10px;">保存</el-button>
          </template>

        </z-detail-page-header>

      </template>

      <div class="code-box">
        <!--      展示-->
        <z-monaco-editor
            v-model:value="state.funcFrom.content"
            v-model:lang="state.lang"
        />
      </div>


    </el-card>

    <el-dialog
        v-if="state.showDiff"
        v-model="state.showDiff"
        title="比对"
        top="5vh"
        width="80%"
        :destroy-on-close="true"

    >
      <template #header>
        <div style="display: flex">
          <span style="font-size: 16px; font-weight: 600; padding-right: 20px">函数比对</span>
          <el-button type="primary" @click="saveOrUpdate">保存</el-button>
        </div>
      </template>
      <div class="diff-box">
        <el-row class="diff-box__title">
          <el-col :span="12"><span style="padding-left: 30px">修改前</span></el-col>
          <el-col :span="12"><span style="padding-left: 15px">修改后</span></el-col>
        </el-row>

        <z-monaco-editor
            :isDiff="true"
            v-model:oldString="state.originalFuncContent"
            v-model:value="state.funcFrom.content"
            v-model:long="state.lang"
        />
      </div>

    </el-dialog>
  </div>
</template>

<script setup name="EditFunc">
import {onMounted, reactive} from "vue";
import {useRoute, useRouter} from 'vue-router'
import {useFunctionsApi} from "/@/api/useAutoApi/functions";
import {ElMessage} from "element-plus/es";

const route = useRoute()
const router = useRouter()
const state = reactive({
  isEdit: true,
  editor: null,
  originalFuncContent: "",
  funcFrom: {
    id: null,
    content: '',
    name: '',
    remarks: ''
  },

  lang: 'python',

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
const showDiffPage = () => {
  if (state.funcFrom.name === "") {
    ElMessage.warning("函数名称不能为空！")
    return
  }
  state.showDiff = !state.showDiff
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

const goBack = () => {
  router.push({name: "ApiFunctions"})
}

// diff
onMounted(() => {
  initData()
})


</script>

<style lang="scss" scoped>

:deep(.el-dialog ) {
  height: calc(100% - 114px);

  .el-dialog__body {
    height: calc(100% - 60px);
  }
}

.code-box {
  height: 100%;
}

.diff-box {
  height: 100%;

  .diff-box__title {
    height: 25px;
  }

  .monaco-editor {
    height: calc(100% - 25px);
  }
}
</style>
