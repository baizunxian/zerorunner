<template>
  <div class="dbTreeForDbQuery">
    <div class="wrapper-op">
      <el-select v-model="state.sourceForm.id"
                 clearable
                 placeholder="请选择数据源"
                 style="width: 100%; margin-left: -1px"
                 @change="sourceChange"
      >
        <el-option
            v-for="item in state.sourceList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
        >
        </el-option>
      </el-select>


      <el-button link type="primary" class="ml10" @click="handelCreatePage">
        <el-icon>
          <ele-CirclePlusFilled/>
        </el-icon>
        新增
      </el-button>
    </div>
    <div class="tree-current-node">
      <span>当前库：</span>{{ state.currentDBRow.name }}
    </div>

    <div class="tree-database-list">
      <el-table
          :data="state.dbList"
          class="w100"
          row-key="name"
          lazy
          highlight-current-row
          :show-header="false"
          :load="loadTableList"
          @row-click="clickDB"
          @row-contextmenu="rowContextmenu"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="name" width="auto" :show-overflow-tooltip="true">
          <template #default="{row}">

            <svg-icon v-if="row.type === 'database'"
                      :size="18"
                      :name="mysqlIcon"
                      align="absmiddle"
                      style="vertical-align: text-bottom;cursor:pointer;"/>
            <svg-icon v-else
                      :size="18"
                      :name="mysqlTableIcon"
                      align="absmiddle"
                      style="vertical-align: text-bottom;cursor:pointer;"/>

            <span style="margin-left: 4px; color: #1f1f1f; font-size: 14px;cursor:pointer;">{{ row.name }}</span>

          </template>
        </el-table-column>
      </el-table>

    </div>

    <SaveOrUpdateSource ref="saveOrUpdateRef" @getList="getSourceList"/>
    <!--右键菜单-->
    <div class="row-contextmenu"
         ref="rowContextmenuRef"
         v-show="state.showRowContextMenu"
         v-click-outside="onClickOutside">
      <div class="row-contextmenu-item row-contextmenu-item-available"
           v-for="item in state.rowContextmenuList"
           :key="item"
           @click="rowContextmenuClick(item)"
      >{{ item.name }}
      </div>
    </div>

    <!--  showCreateTable  -->
    <el-dialog v-model="state.showCreateTable" :title="`建表语句：${(state.rightClickRow.name)}`">
      <z-monaco-editor
          :style="{height: '500px'}"
          ref="monacoEditRef"
          v-model:value="state.createTableContent"
          lang="sql"
      ></z-monaco-editor>
    </el-dialog>

  </div>

</template>

<script setup name="DBList">
import {nextTick, onMounted, onUnmounted, reactive, ref} from 'vue';
import {useQueryDBApi} from "/@/api/useTools/querDB";
import mysqlIcon from "/@/icons/mysql_icon.svg";
import mysqlTableIcon from "/@/icons/mysql_table.svg";
import mittBus from '/@/utils/mitt';
import {useThemeConfig} from "/@/stores/themeConfig";
import {storeToRefs} from "pinia";
import SaveOrUpdateSource from "/@/views/api/dataSource/EditDataSource.vue";
// 定义变量内容
const storesThemeConfig = useThemeConfig();
const {themeConfig} = storeToRefs(storesThemeConfig);

const saveOrUpdateRef = ref()
const rowContextmenuRef = ref()

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
  currentDBRow: {},
  // table
  tableList: [],
  tableForm: {
    source_id: null,
    databases: null,
    table: null,
  },

  // column
  showRowContextMenu: false,
  showCreateTable: false,
  createTableContent: "",
  rightClickRow: {},
  rowContextmenuList: [
    {name: "查看建表语句", value: 'view_create_table_sql'},
    {name: "生成select*语句", value: 'generate_select_sql'},
  ],

});
// source
const getSourceList = () => {
  useQueryDBApi().getSourceList(state.sourceForm).then((res) => {
    state.sourceList = res.data.rows
  })
}

// source 变更
const sourceChange = (value) => {
  state.dbForm.source_id = state.tableForm.source_id = value
  if (!value) {
    state.sourceForm.id = null
    state.dbList = []
    state.tableList = []
    state.currentDBRow = {}
  } else {
    getDBList()
  }
}

// 获取数据库列表
const getDBList = () => {
  useQueryDBApi().getDBList(state.dbForm).then((res) => {
    state.dbList = res.data
  })
}

// 点击数据库
const clickDB = async (row, column, event) => {
  console.log("clickDB", row, column, event)
  let iconInfo = event.currentTarget.querySelector(".el-table__expand-icon")
  if (iconInfo) {
    iconInfo.click();
  }
  if (row.type === "database") {
    let data
    if (row.db_data) {
      data = row.db_data
    } else {
      let dbs = await getColumnList()
      row.db_data = data = {
        database: row.name,
        source_id: state.sourceForm.id,
        dbs: [{dbName: row.name, tables: dbs}]
      }
    }
    state.currentDBRow = row
    state.tableForm.databases = row.name
    mittBus.emit("setSourceInfo", data)
  }
}

// 加载数据库列表
const getTableList = async (databases = "") => {
  if (databases) state.tableForm.databases = databases
  let res = await useQueryDBApi().getTableList(state.tableForm)
  return res.data
}

// 加载数据库列表
const loadTableList = async (row, treeNode, resolve) => {
  state.tableForm.databases = row.name
  let tableList = await getTableList()
  resolve(tableList)
}

// 获取字段列表
const getColumnList = async (table = null) => {
  if (table) {
    state.tableForm.table = table
  } else {
    state.tableForm.table = null
  }
  let res = await useQueryDBApi().getColumnList(state.tableForm)
  return res.data
}

// 打开数据源新增页面
const handelCreatePage = () => {
  saveOrUpdateRef.value.openDialog("save")
}

const rowContextmenu = (row, column, event) => {
  event.preventDefault();
  if (row.type === 'table') {
    state.showRowContextMenu = true
    state.rightClickRow = row
    nextTick(() => {
      let {isCollapse} = themeConfig.value;
      let sidebarWidth = isCollapse ? 64 : 220
      let headerWidth = isCollapse ? 87 : 87
      rowContextmenuRef.value.style.left = `${event.clientX - sidebarWidth}px`;
      rowContextmenuRef.value.style.top = `${event.clientY - headerWidth}px`;
    })
  }
}

const rowContextmenuClick = async (item) => {
  if (item.value === 'view_create_table_sql') {
    let params = {
      source_id: state.sourceForm.id,
      databases: state.currentDBRow.name,
      table_name: state.rightClickRow.name
    }
    let {data} = await useQueryDBApi().showCreateTable(params)
    state.createTableContent = data.create_table_sql
    state.showCreateTable = true
  } else if (item.value === "generate_select_sql") {
    mittBus.emit("setSql", "select * from " + `${state.rightClickRow.name} limit 20;`)
  }
  state.showRowContextMenu = false
}

const onClickOutside = () => {
  state.showRowContextMenu = false
}

onMounted(() => {
  getSourceList()

  mittBus.on("getColumnList", async (table) => {
    let res = await getColumnList(table)
    return res
    // await getColumnList(table).then(async (res) => {
    //   console.log("table--------------->", res)
    //   return res
    // })
  })
})

onUnmounted(() => {
  mittBus.off("getColumnList")
})

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

    span {
      color: #2c2f37;
      font-weight: 600;
      font-size: 12px
    }
  }

  .tree-database-list {
    height: calc(100% - 70px);
    overflow-y: auto;
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

.row-contextmenu {
  z-index: 2043;
  width: 150px;
  position: absolute;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color-light);
  min-width: 150px;
  //color: var(--el-text-color-regular);
  text-align: justify;
  box-shadow: var(--el-box-shadow-light);
  word-break: break-all;
  box-sizing: border-box;
  border-radius: var(--el-popper-border-radius);
  line-height: 20px;
  word-wrap: break-word;
  visibility: visible;

  .row-contextmenu-item {
    list-style: none;
    line-height: 32px;
    padding: 0 16px;
    margin: 0;
    font-size: 13px;
    outline: 0;
    display: flex;
    align-items: center;
    transition: .2s;
    border-bottom: 1px solid transparent;
  }

  .row-contextmenu-item-available {
    color: #606266;
    cursor: pointer;

    &:hover {
      background: #ecf5ff;
      color: #409eff;
    }
  }
}

</style>