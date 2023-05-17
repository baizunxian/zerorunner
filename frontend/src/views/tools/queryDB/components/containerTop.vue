<template>
  <div>
    <div class="db-query-top-bar">
      <el-button link type="primary" @click="execute">
        <el-icon>
          <ele-CaretRight/>
        </el-icon>
        执行
      </el-button>
    </div>

    <div style="border: 1px solid #E6E6E6; overflow-y: auto">
      <z-monaco-editor
          ref="monacoEditRef"
          :style="{height: state.height + 'px'}"
          :dbs="state.dbs"
          v-model:value="state.sql"
          v-model:long="state.long"
          :onInputTableAlia="onInputTableAlia"
          :executeHandle="execute"
      ></z-monaco-editor>
    </div>
  </div>
</template>

<script lang="ts" setup name="ContainerTop">
import {computed, onBeforeMount, onUnmounted, reactive, ref} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {ElMessage} from "element-plus/es";
import {ElLoading} from "element-plus";
import mittBus from '/@/utils/mitt';

const monacoEditRef = ref()

const state = reactive({
  long: 'sql',
  height: 300,
  // db
  dbs: [],
  //execute
  sql: 'select  * from ',
  executeForm: {
    sql: '',
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


const setSql = (sql: string) => {
  if (state.sql === "") {
    state.sql = sql
  } else {
    state.sql = `${state.sql}\n${sql}`
  }
}

const execute = () => {
  if (state.sql === "") {
    ElMessage.warning("请输入sql语句查询！")
    return;
  }
  if (state.executeForm.source_id == "") {
    ElMessage.warning('请选择对应数据源！');
    return
  }
  const loading = ElLoading.service({text: "sql执行中...", target: monacoEditRef.value.$el})
  try {
    let selectionSql = monacoEditRef.value.getSelectionValue()
    if (selectionSql !== "") {
      state.executeForm.sql = selectionSql
    } else {
      state.executeForm.sql = state.sql
    }
    useQueryDBApi().execute(state.executeForm).then((res: any) => {
      mittBus.emit("setExecuteResult", res.data)
    })

  } catch (err) {
    console.log(err)
  } finally {
    loading.close()
  }
}

const onInputTableAliaData = computed(() => {
  console.log('22222222222222222222')
  return []
})

const onInputTableAlia = async (table: any) => {
  console.log("databases----------->", table)
  let res = await mittBus.emit("getColumnList", (table: any) => {
    console.log("table------------table", table)
  })
  console.log("res------------res", res)
  return []
}
onBeforeMount(() => {
  mittBus.on('setSourceInfo', (data: any) => {
    setData(data)
  })
  mittBus.on('setSql', (data: any) => {
    setSql(data)
  })
})

onUnmounted(() => {
  mittBus.off("setSourceInfo", () => {
  })
  mittBus.off("setSql", () => {
  })
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
  padding-bottom: 10px;
}

</style>