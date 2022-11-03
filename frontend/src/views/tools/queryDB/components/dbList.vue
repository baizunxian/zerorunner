<template>
  <div class="dbTreeForDbQuery">
    <div class="wrapper-op">
      <!--      <el-select v-model="dbForm.data_source"-->
      <!--                 clearable placeholder="请选择数据库"-->
      <!--                 style="width: 200px"-->
      <!--                 @change="sourceChange"-->
      <!--      >-->
      <!--        <el-option-->
      <!--            v-for="item in dataSource"-->
      <!--            :key="item"-->
      <!--            :label="item"-->
      <!--            :value="item"-->
      <!--        >-->
      <!--        </el-option>-->
      <!--      </el-select>-->
      <el-select v-model="sourceForm.id"
                 clearable
                 placeholder="请选择数据源"
                 style="width: 200px; margin-left: -1px"
                 @change="sourceChange"
      >
        <el-option
            v-for="item in sourceList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
        >
        </el-option>
      </el-select>


      <el-button link type="primary"  class="ml10" @click="handelCreatePage">
        <el-icon>
          <ele-CirclePlusFilled/>
        </el-icon>
        新增
      </el-button>
    </div>
    <div class="tree-current-node">
      <span style="color: #2c2f37;font-weight: 600; font-size: 12px">当前库：</span>{{ currentDB }}
    </div>

    <div style="height: 100%; overflow-y: auto">
      <el-table
          :data="dbList"
          style="width: 100%"
          row-key="name"
          lazy
          :show-header="false"
          :load="loadTableList"
          @row-click="clickDB"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="name" width="auto" :show-overflow-tooltip="true">
          <template #default="{row}">
            <svg-icon v-if="row.type === 'database'" :size="18" :name="mysqlIcon" align="absmiddle"
                      style="vertical-align: text-bottom;"/>
            <svg-icon v-else :size="18" :name="mysqlTableIcon" align="absmiddle" style="vertical-align: text-bottom;"/>
            <span style="margin-left: 4px; color: #1f1f1f; font-size: 14px">{{ row.name }}</span>
          </template>
        </el-table-column>
      </el-table>

    </div>

    <save-or-update-source ref="saveOrUpdateRef" @getList="getSourceList"/>

  </div>

</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs, ref, getCurrentInstance, onUnmounted} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import mysqlIcon from "/@/icons/mysql_icon.svg";
import mysqlTableIcon from "/@/icons/mysql_table.svg";
import saveOrUpdateSource from "/@/views/tools/dataSource/components/saveOrUpdate.vue";

export default defineComponent({
  name: 'typeTab',
  components: {
    saveOrUpdateSource,
  },
  setup() {
    const {proxy} = <any>getCurrentInstance();

    const saveOrUpdateRef = ref()

    const state = reactive({
      // source
      sourceList: [],
      sourceForm: {
        id: null,
      },
      dataSourceForm: {
        id: null,
        name: "",
        type: "mysql",
        host: "",
        port: "",
        user: "",
        password: "",
      },
      // db
      dbList: [],
      dbForm: {
        id: null,
        source_id: null,
      },
      currentDB: '',
      // table
      tableList: [],
      tableForm: {
        source_id: null,
        databases: null,
      },

      // column
    });
    // source
    const getSourceList = () => {
      useQueryDBApi().getSourceList(state.sourceForm).then((res: any) => {
        state.sourceList = res.data
      })
    }

    // source 变更
    const sourceChange = (value: string) => {
      state.dbForm.source_id = state.tableForm.source_id = value
      if (!value) {
        state.sourceForm.id = null
        state.dbList = []
        state.tableList = []
      } else {
        getDBList()
      }
    }

    // 获取数据库列表
    const getDBList = () => {
      useQueryDBApi().getDBList(state.dbForm).then((res: any) => {
        state.dbList = res.data
      })
    }

    // 点击数据库
    const clickDB = async (row: any, column, event) => {
      let iconInfo = event.currentTarget.querySelector(".el-table__expand-icon")
      if (iconInfo) {
        iconInfo.click();
      }
      console.log(row, column, event)
    }

    // 加载数据库列表
    const getTableList = async (databases: string = "") => {
      if (databases) state.tableForm.databases = databases
      let res = await useQueryDBApi().getTableList(state.tableForm)
      return res.data
    }

    // 加载数据库列表
    const loadTableList = async (row: any, treeNode: unknown, resolve: (date: any) => void) => {
      state.tableForm.databases = row.name
      let tableList: any = await getTableList()
      if (row.type === "database") {
        state.tableForm.databases = row.name
        state.currentDB = row.name
        let dbs = await getColumnList()
        let data = {
          database: row.name,
          source_id: state.sourceForm.id,
          dbs: [{dbName: row.name, tables: dbs}]
        }
        proxy.mittBus.emit("setSourceInfo", data)
        // emit("setData", data)
      }
      // return tableList
      resolve(tableList)
    }

    // 获取字段列表
    const getColumnList = async (table: any) => {
      if (table) {
        state.tableForm.table = table
      } else {
        state.tableForm.table = null
      }
      let res: any = await useQueryDBApi().getColumnList(state.tableForm)
      return res.data
    }

    const handleCheckChange = (
        data: any,
        checked: boolean,
        indeterminate: boolean
    ) => {
      console.log(data, checked, indeterminate)
    }

    // 打开数据源新增页面
    const handelCreatePage = () => {
      saveOrUpdateRef.value.openDialog("save")
    }

    const saveOrUpdateSource = () => {
      useQueryDBApi().saveOrUpdate()
    }

    onMounted(() => {
      getSourceList()

      proxy.mittBus.on("getColumnList", async (table: any) => {
        await getColumnList(table).then(async (res) => {
          console.log("table--------------->", res)
          return res
        })
      })
    })

    onUnmounted(() => {
      proxy.mittBus.off("getColumnList")
    })

    return {
      getSourceList,
      getDBList,
      getColumnList,
      clickDB,
      getTableList,
      loadTableList,
      sourceChange,
      handleCheckChange,
      mysqlIcon,
      mysqlTableIcon,
      saveOrUpdateRef,
      handelCreatePage,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

.dbTreeForDbQuery {
  padding: 0 6px;
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  height: 100%;

  .wrapper-op {
    min-width: 220px;
    margin-bottom: 8px;
    display: flex;
    //flex-direction: column;
    align-items: stretch;
  }

  .tree-current-node {
    padding: 0 0 8px 6px;
    border-bottom: 1px solid #dee2ea;
    margin-bottom: 6px;
  }
}

.el-tree .el-icon i { //原有的箭头 去掉
  display: none !important;
  height: 0;
  width: 0;
}

:deep(.el-table td.el-table__cell) {
  border-bottom: #ffffff;
}

:deep(.el-table__inner-wrapper::before) {
  content: "";
  position: absolute;
  background-color: #FFFFFF;
  z-index: 10;
}

//:deep(.el-table__empty-block) {
//  ::before {
//    content: "";
//    position: absolute;
//    background-color: #FFFFFF;
//    z-index: 10;
//  }

//}


</style>