<template>
  <el-dialog
      draggable
      v-model="state.showRelationGraph"
      width="80%"
      class="relation-draggable"
      top="5vh"
      destroy-on-close
      :close-on-click-modal="false">
    <template #header>
      <strong>血缘关系</strong>
    </template>
    <div class="h100">
      <div class="relationGraphHeader">
        <div class="label-itme" v-show="state.relationGraphData?.api_count && state.relationGraphData.type !== 'api'">
          <el-button style="width: 20px; height: 15px"
                     :style="{backgroundColor: getStepTypeInfo('api', 'color')}"></el-button>
          <span class="label-itme-text">接口数：{{ state.relationGraphData?.api_count }}</span>
        </div>
        <div class="label-itme" v-show="state.relationGraphData?.case_count && state.relationGraphData.type !== 'case'">
          <el-button style="width: 20px; height: 15px"
                     :style="{backgroundColor: getStepTypeInfo('case', 'color')}"></el-button>
          <span class="label-itme-text">用例数：{{ state.relationGraphData?.case_count }}</span>
        </div>
        <div class="label-itme"
             v-show="state.relationGraphData?.timed_task_count && state.relationGraphData.type !== 'timed_task'">
          <el-button style="width: 20px;height: 15px"
                     :style="{backgroundColor: getStepTypeInfo('timed_task', 'color')}"></el-button>
          <span class="label-itme-text">定时任务数：{{ state.relationGraphData?.timed_task_count }}</span>
        </div>
<!--        <el-button style="width: 20px;height: 15px" @click="setNode"-->
<!--        >设置节点-->
<!--        </el-button>-->
      </div>

      <div class="relationGraphBox" ref="relationGraphBox" @click="state.isShowNodeMenuPanel = false">
        <RelationGraph ref="relationGraph$" :options="state.graphOptions">
          <template #node="{node}">

            <div class="node-box"
                 @contextmenu.prevent.stop="showNodeMenus(node, $event)"
                 :style="{backgroundColor:getStepTypeInfo(node.data.type, 'color')}">
              <div class="node-header">
                <i :class="getStepTypeInfo(node.data.type,'icon')" class="fab-icons"
                   :style="{color:'#FFFFFF', fontSize: '24px'}">
                </i>
                <span :title="node.data.name" class="node-header-text">
                {{ node.data.name }}</span>
              </div>
              <div class="node-body">
                <div class="node-text">
                  <label>类型：</label>
                  <span>{{ node.data.type }}</span>
                </div>
                <div class="node-text">
                  <label>创建人：</label>
                  <span>{{ node.data.created_by_name }}</span>
                </div>
                <div class="node-text">
                  <label>创建时间：</label>
                  <span>{{ node.data.creation_date }}</span>
                </div>
              </div>
            </div>
          </template>

        </RelationGraph>
      </div>

      <div>
        <div v-show="state.isShowNodeMenuPanel"
             class="node-menu-box"
             :style="{left: state.nodeMenuPanelPosition.x + 'px', top: state.nodeMenuPanelPosition.y + 'px' }">
          <div class="node-menu-item node-menu-item__available" @click.stop="jumpTo">跳转</div>
          <div class="node-menu-item node-menu-item__available" @click.stop="toSelectedNode">跳转到当前节点</div>
        </div>
      </div>

      <div>
        <div v-if="state.isShowNodeTipsPanel"
             :style="{left: state.nodeMenuPanelPosition.x + 'px', top: state.nodeMenuPanelPosition.y + 'px' }"
             style="z-index: 999;padding:10px;background-color: #ffffff;border:#eeeeee solid 1px;box-shadow: 0px 0px 8px #cccccc;position: absolute;">
          <div style="line-height: 25px;padding-left: 10px;color: #888888;font-size: 12px;">
            节点名称：{{ state.currentNode.text }}
          </div>
          <div class="c-node-menu-item">id:{{ state.currentNode.text }}</div>
          <div class="c-node-menu-item">图标:{{ state.currentNode.data?.myicon }}</div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup name="ApiRelationGraph">
// 接口关系
import {nextTick, reactive, ref} from "vue";
import RelationGraph from 'relation-graph/vue3'
import {getStepTypeInfo} from "/@/utils/case";
import {useRouter} from "vue-router";
import {useRelationGraphApi} from "/@/api/useAutoApi/relationGraph";

const router = useRouter()

const relationGraphBox = ref()
const relationGraph$ = ref()

const state = reactive({
  relationGraphData: {},
  // data
  showRelationGraph: false,
  showMenu: false,
  isShowNodeMenuPanel: false,
  isShowNodeTipsPanel: false,
  currentNode: {},
  nodeMenuPanelPosition: {
    x: 0,
    y: 0
  },
  graphOptions: {
    // http://relation-graph.com/#/docs/graph  配置说明
    // defaultExpandHolderPosition: 'right',
    // defaultLineShape: 4,
    defaultLineWidth: 2,
    debug: false,
    showDebugPanel: false,
    // defaultNodeShape: 1,
    // defaultNodeColor: '#ffffff',
    // defaultNodeBorderWidth: 0,
    // defaultNodeBorderColor: '#ffffff',
    // defaultJunctionPoint: 'border',
    allowSwitchLineShape: true,
    allowSwitchJunctionPoint: true,
    defaultLineColor: 'rgba(16,9,9,0.6)',
    defaultNodeColor: 'transparent',
    defaultNodeBorderWidth: 0,
    defaultNodeBorderColor: 'transpanret',
    defaultNodeFontColor: '#ffffff',
    defaultNodeShape: 1,
    toolBarDirection: 'h',
    toolBarPositionH: 'right',
    toolBarPositionV: 'bottom',
    defaultPloyLineRadius: 10,
    defaultLineShape: 6,
    defaultJunctionPoint: 'lr',
    'layouts': [
      {
        layoutName: 'tree',
        from: 'left',
        levelDistance: "350,350,350,500",
        'min_per_width': 600, // 根据节点的宽度设置，这个是让图谱看起来偏亮的关键
        'min_per_height': 80,

      }
    ],
  },
  relationForm: {
    id: null,
    type: null
  }
});

const initData = () => {
  useRelationGraphApi().getRelationGraph(state.relationForm).then(res => {
    state.relationGraphData = res.data
    relationGraph$.value.setJsonData(state.relationGraphData, () => {
    })
  })

  nextTick(() => {
    relationGraph$.value.onGraphResize()
    relationGraph$.value.refresh()
  })
}

const setNode = () => {
  // relationGraph$.value.getInstance().setCheckedNode("api_1")
  console.log(relationGraph$.value.getInstance().getNodes())
  const nodes = relationGraph$.value.getInstance().getNodes()
  nextTick(() => {
    relationGraph$.value.getInstance().setCheckedNode("api_1")
    // relationGraph$.value.refresh()
  })

}

const openDialog = (id, type) => {
  state.relationForm.id = id
  state.relationForm.type = type
  state.showRelationGraph = true
  initData()
}

const showMenu = () => {
  state.showMenu = !state.showMenu
}


const onNodeClick = (nodeObject, $event) => {
}

const showNodeMenus = (nodeObject, $event) => {
  state.currentNode = nodeObject;
  const _base_position = relationGraphBox.value.getBoundingClientRect();
  state.isShowNodeMenuPanel = true;
  state.nodeMenuPanelPosition.x = $event.clientX - _base_position.x + 10;
  state.nodeMenuPanelPosition.y = $event.clientY - _base_position.y + 60;
}

const nodeSlotOver = (nodeObject, $event) => {
  state.currentNode = nodeObject;
  const _base_position = relationGraphBox.value.getBoundingClientRect();
  state.isShowNodeTipsPanel = true;
  state.nodeMenuPanelPosition.x = $event.clientX - _base_position.x + 10;
  state.nodeMenuPanelPosition.y = $event.clientY - _base_position.y + 60;
}

const nodeSlotOut = (nodeObject, $event) => {
  state.isShowNodeTipsPanel = false;
}

const doAction = (actionName) => {
  state.isShowNodeMenuPanel = false;
}

const jumpTo = () => {
  const query = {editType: 'edit', id: state.currentNode.data.id}
  switch (state.currentNode.data?.type) {
    case "api":
      router.push({name: 'EditApiInfo', query: query})
      break
    case "case":
      router.push({name: 'EditApiCase', query: query})
      break
    default:
      break
  }
  state.isShowNodeMenuPanel = false;
}


const toSelectedNode = () => {
  state.relationForm.id = state.currentNode.data.id
  state.relationForm.type = state.currentNode.data.type
  initData()
  state.isShowNodeMenuPanel = false;
}

defineExpose({
  showMenu,
  openDialog
})

</script>
<style>
.relation-draggable .el-dialog__body {
  height: 80vh;
}
</style>

<style lang="scss" scoped>

.node-box {
  cursor: pointer;
  background-color: #30bf78;
  padding: 2px;
  text-align: left;
  width: 200px;
  border-radius: 5px;

  .node-header {
    height: 30px;
    line-height: 30px;
    //padding-left: 10px;
    .node-header-text {
      padding-left: 10px;
      line-height: 30px;
      position: absolute;
      overflow: hidden; //隐藏文字
      text-overflow: ellipsis; //显示...
      white-space: nowrap; //不换行
      width: 160px;
    }
  }

  .node-body {
    line-height: 16px;
    height: 50px;
    background-color: #FFFFFF;
    border-radius: 0 0 5px 5px;

    .node-text {
      font-size: 12px;
      overflow: hidden; //隐藏文字
      text-overflow: ellipsis; //显示...
      white-space: nowrap; //不换行
      //width: 160px;
      color: #606266;
    }
  }

}

.node-menu-box {
  z-index: 999;
  background-color: #ffffff;
  border: #eeeeee solid 1px;
  box-shadow: 0px 0px 8px #cccccc;
  position: absolute;
  min-width: 160px;
}

.node-menu-item {
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

.node-menu-item__available {
  cursor: pointer;
}

.node-menu-item__available:hover {
  background: #ecf5ff;
  color: #409eff;
}

.relationGraphHeader {
  height: 30px;
  line-height: 30px;
  width: 100%;
  display: flex;
  align-content: center;

  .label-itme {
    padding-right: 10px;

    .label-itme-text {
      padding-left: 5px;
      font-size: 12px;
    }
  }
}

.relationGraphBox {
  height: calc(100% - 30px);
}

</style>