<template>
  <div class="h100">
    <div class="h100" ref="relationGraphBox" @click="state.isShowNodeMenuPanel = false">
      <RelationGraph ref="relationGraph$" :options="state.graphOptions">
        <template #node="{node}">

          <div style="width:200px;cursor: pointer; color: black">
              {{node.data.name}}
          </div>
          <!--          <div @mouseover="nodeSlotOver(node, $event)"-->
          <!--               @mouseout="nodeSlotOut(node, $event)"-->
          <!--               @contextmenu.prevent.stop="showNodeMenus(node, $event)"-->
          <!--          >-->
          <!--            <div-->
          <!--                style="height:80px;line-height: 80px;border-radius: 50%;cursor: pointer;">-->
          <!--              <i style="font-size: 30px;" :class="node.data.myicon"/>-->
          <!--            </div>-->
          <!--            <div-->
          <!--                style="-->
          <!--                        color: forestgreen;-->
          <!--                        font-size:-->
          <!--                        16px;position: absolute;-->
          <!--                        width: 160px;-->
          <!--                        height:25px;line-height: 25px;margin-top:5px;margin-left:-48px;text-align: center;background-color: rgba(66,187,66,0.2);">-->
          <!--              {{ node.text }}-->
          <!--            </div>-->
          <!--          </div>-->
        </template>

      </RelationGraph>
    </div>

    <div>
      <div v-show="state.isShowNodeMenuPanel"
           :style="{left: state.nodeMenuPanelPosition.x + 'px', top: state.nodeMenuPanelPosition.y + 'px' }"
           style="z-index: 999;padding:10px;background-color: #ffffff;border:#eeeeee solid 1px;box-shadow: 0px 0px 8px #cccccc;position: absolute;">
        <div style="line-height: 25px;padding-left: 10px;color: #888888;font-size: 12px;">对这个节点进行操作：</div>
        <div class="c-node-menu-item" @click.stop="doAction('操作1')">操作1</div>
        <div class="c-node-menu-item" @click.stop="doAction('操作1')">操作2</div>
        <div class="c-node-menu-item" @click.stop="doAction('操作1')">操作3</div>
        <div class="c-node-menu-item" @click.stop="doAction('操作1')">操作4</div>
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
</template>

<script setup name="RelationGraph">
import {onMounted, reactive, ref, watch, nextTick} from "vue";
import RelationGraph from 'relation-graph/vue3'

const relationGraphBox = ref()
const relationGraph$ = ref()

const props = defineProps({
  data: {
    type: Object,
    default: () => []
  }
})

const state = reactive({
  // data
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
    debug: false,
    showDebugPanel: false,
    defaultNodeShape: 1,
    defaultNodeColor: '#ffffff',
    defaultNodeBorderWidth: 1,
    defaultNodeBorderColor: '#ffffff',
    defaultJunctionPoint: 'border',
    'layouts': [
      {
        'label': '中心',
        'layoutName': 'center',
        'layoutClassName': 'seeks-layout-center'
      }
    ],
  },
});

const initData = () => {
  relationGraph$.value.setJsonData(props.data, () => {
  })
  nextTick(() => {
    relationGraph$.value.onGraphResize()
    relationGraph$.value.refresh()
  })
}

onMounted(() => {
  initData()
})

const showMenu = () => {
  state.showMenu = !state.showMenu
}


const onNodeClick = (nodeObject, $event) => {
}

const showNodeMenus = (nodeObject, $event) => {
  state.currentNode = nodeObject;
  const _base_position = relationGraphBox.value.getBoundingClientRect();
  state.isShowNodeMenuPanel = true;
  state.nodeMenuPanelPosition.x = $event.clientX - _base_position.x + 30;
  state.nodeMenuPanelPosition.y = $event.clientY - _base_position.y + 30;
}

const nodeSlotOver = (nodeObject, $event) => {
  state.currentNode = nodeObject;
  const _base_position = relationGraphBox.value.getBoundingClientRect();
  state.isShowNodeTipsPanel = true;
  state.nodeMenuPanelPosition.x = $event.clientX - _base_position.x + 30;
  state.nodeMenuPanelPosition.y = $event.clientY - _base_position.y + 30;
}

const nodeSlotOut = (nodeObject, $event) => {
  state.isShowNodeTipsPanel = false;
}

const doAction = (actionName) => {
  state.isShowNodeMenuPanel = false;
}


watch(
    () => props.data,
    () => {
      nextTick(() => {
        initData()
      })
    },
    {deep: true}
)

defineExpose({
  showMenu
})

</script>

<style lang="scss" scoped>

</style>