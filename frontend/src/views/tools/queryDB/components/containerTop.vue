<template>
  <div>
    <div class="db-query-top-bar">
      <el-link @click="execute">
        <el-icon>
          <ele-CaretRight/>
        </el-icon>
        执行
      </el-link>
    </div>

    <div style="border: 1px solid #E6E6E6; overflow-y: auto" ref="monacoEditDivRef">
      <z-monaco-editor
          :style="{height: state.height + 'px'}"
          ref="monacoEditRef"
          :dbs="state.dbs"
          v-model:value="state.executeForm.sql"
          v-model:long="state.long"
          :onInputTableAlia="onInputTableAlia"
      ></z-monaco-editor>
    </div>
  </div>
</template>

<script lang="ts" setup name="ContainerTop">
import {onMounted, onUnmounted, reactive, ref} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {ElMessage} from "element-plus/es";
import {ElLoading} from "element-plus";
import mittBus from '/@/utils/mitt';

const monacoEditDivRef = ref()
const monacoEditRef = ref()

const state = reactive({
  long: 'sql',
  height: 300,
  // db
  dbs: [],
  //execute
  executeForm: {
    sql: 'select  * from ',
    source_id: "",
    database: "",
  }
});

const setMonacoHeHeight = (height: number) => {
  state.height = height
}

const setData = (data: any) => {
  state.dbs = data.dbs
  state.executeForm.source_id = data.source_id
  state.executeForm.database = data.database
}

const execute = async () => {
  if (state.executeForm.source_id == "") {
    ElMessage.warning('请选择对应数据源！');
    return
  }
  const loading = ElLoading.service({text: "sql执行中...", target: monacoEditRef.value.$el})
  try {
    let res = await useQueryDBApi().execute(state.executeForm)
    mittBus.emit("setExecuteResult", res.data)
  } catch (err) {
    console.log(err)
  } finally {
    loading.close()
  }
}

const onInputTableAlia = async (table: any) => {
  console.log("databases----------->", table)
  let res = await mittBus.emit("getColumnList", (table) => {
    console.log("table------------table", table)
  })
  console.log("res------------res", res)
  return res
}
onMounted(() => {
  mittBus.on("setSourceInfo", (data: any) => {
    setData(data)
  })
})

onUnmounted(() => {
  mittBus.off("setSourceInfo")
})


defineExpose({
  setMonacoHeHeight,
})

</script>

<style lang="scss" scoped>

.db-query-top-bar {
  flex: none;
  display: flex;
  border-bottom: 1px solid #dee2ea;
  padding: 0 2px;
}

</style>