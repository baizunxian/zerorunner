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
      <monaco-editor
          :style="{height: height + 'px'}"
          ref="monacoEditRef"
          :dbs="dbs"
          v-model:value="executeForm.sql"
          v-model:long="long"
          :onInputTableAlia="onInputTableAlia"
      ></monaco-editor>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs, ref, getCurrentInstance, onMounted, onUnmounted} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import {ElMessage} from "element-plus/es";
import {ElLoading} from "element-plus";

export default defineComponent({
  name: 'app',
  setup() {
    const monacoEditDivRef = ref()
    const monacoEditRef = ref()
    const {proxy} = <any>getCurrentInstance();
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
      state.executeForm.sql = monacoEditRef.value.getValue()
      const loading = ElLoading.service({text: "sql执行中...", target: monacoEditRef.value.$el})
      try {
        let res = await useQueryDBApi().execute(state.executeForm)
        proxy.mittBus.emit("setExecuteResult", res.data)
      } catch (err) {
        console.log(err)
      } finally {
        loading.close()
      }
    }

    const onInputTableAlia = async (table: any) => {
      console.log("databases----------->", table)
      let res = await proxy.mittBus.emit("getColumnList", (table) => {
        console.log("table------------table", table)
      })
      console.log("res------------res", res)
      return res
    }
    onMounted(() => {
      proxy.mittBus.on("setSourceInfo", (data: any) => {
        setData(data)
      })
    })

    onUnmounted(() => {
      proxy.mittBus.off("setSourceInfo")
    })

    return {
      setData,
      execute,
      monacoEditRef,
      monacoEditDivRef,
      onInputTableAlia,
      setMonacoHeHeight,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

.db-query-top-bar {
  flex: none;
  display: flex;
  border-bottom: 1px solid #dee2ea;
  padding: 0 2px;
}

</style>