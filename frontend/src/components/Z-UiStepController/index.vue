<template>
  <div class="h100" id="stepController" style="overflow-y: auto">
    <el-backtop :right="200" :bottom="200" :visibility-height="10" target="#stepController"/>
    <div class="h100" style="overflow-y: auto;">

      <el-tree
          ref="stepTreeRef"
          draggable
          highlight-current
          :allow-drop="allowDrop"
          @node-click="nodeClick"
          node-key="id"
          @node-drag-start="handleDrop"
          :expand-on-click-node="false"
          :data="data">
        <template #default="{ node }">
          <StepNode v-model:data="node.data"
                    :node="node"
                    :class="[node.data.step_type ==='case'?'treeCaseStep':'']"
                    :opt-type="state.optTypes"
                    @copy-node="copyNode"
                    @deleted-node="deletedNode(node)"
          />
        </template>
      </el-tree>
      <el-backtop target=".el-tree"/>
    </div>

    <UiInfoController ref="UiInfoDetailRef"></UiInfoController>

  </div>
</template>

<script setup name="uiStepController">
import {onMounted, reactive, ref} from 'vue';
import StepNode from "./StepNode.vue";
import UiInfoController from "/@/components/Z-UiStepController/uiStepInfo/UiInfoController.vue";


const emit = defineEmits([])

const props = defineProps({
  use_type: {
    type: String,
    default: () => {
      return 'pre'   // pre 前置  post 候置  case 用例
    }
  },
  data: {
    type: Array,
    default: () => []
  },
  case_id: {
    type: [Number, String, null],
    default: () => {
      return null
    }
  }
})

const UiInfoDetailRef = ref()
// const selectApiRef = ref()
const stepTreeRef = ref()

const state = reactive({
  // data
  optType: "script",
  optTypes: {},
  // caseInfo
  showApiInfo: false,

});


// 拖动处理
const allowDrop = (draggingNode, dropNode, type) => {
  // if (dropNode.data.step_type === 'if' && type === 'inner') {
  //   return true
  // } else if (dropNode.data.step_type === 'loop' && type === 'inner') {
  //   return true
  // }
  // return type
  return type !== "inner"
}

// 节点拖动完成重新计算顺序
const handleDrop = (node, event) => {
  // return false
}

const nodeClick = (data, node) => {
  UiInfoDetailRef.value.onOpenApiInfoPage(data)
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data) => {
  if (data) {
    data.forEach((data, index) => {
      data.index = index + 1
      if (data.sub_steps) {
        computeDataIndex(data.sub_steps)
      }
    })
  }
}
// handleAddData
const handleAddData = async () => {
  let stepData = await getStepData()
  addData(stepData)
}

// 添加tree data
const addData = () => {
  let stepData = getStepData()
  stepTreeRef.value.append(stepData, null)
}

const getStepData = () => {
  let stepData = {
    id: null,
    name: "",
    case_id: null,
    enable: true,
    index: 0,
    step_type: "",
    variables: [],
    setup_hooks: [],
    teardown_hooks: [],
    extracts: [],
    export: [],
    validators: [],
    request: null,
    sql_request: null,
    loop_request: null,
    if_request: null,
    wait_request: null,
    script_request: null,
    ui_request: {
      action: "",
      input_data: "",
      location_method: "",
      location_value: "",
      cookie: "",
      output: ""
    },
    showDetail: false,
  }
  return stepData
}

const deletedNode = (node) => {
  stepTreeRef.value.remove(node)
  // props.data.splice(index, 1)
}
const copyNode = (data) => {
  props.data.push(JSON.parse(JSON.stringify(data)))
}


onMounted(() => {
})

defineExpose({
  addData,
})

</script>

<style lang="scss" scoped>

:deep(.el-overlay .el-dialog .el-dialog__body) {
  padding: 0 !important;
}

// el-terr
:deep(.el-tree-node__content) {
  height: 100%;
  margin-top: 6px;
  vertical-align: center;
  display: flex;
  cursor: pointer;
  align-items: center;
}

:deep(.el-tree-node__label) {
  width: 100%;
}

:deep(.el-input--small .el-input__inner) {
  --el-input-inner-height: calc(var(--el-input-height, 24px) - 1px);
}

.el-tree {
  padding: 10px;
  background: transparent !important;
}

:deep(.el-tree-node__expand-icon) {
  // 更换图标库
  font-family: "iconfont" !important;

  svg {
    display: none;
  }

  color: #1f1f1f;
  font-style: normal;
}

:deep(.el-tree-node__expand-icon.expanded) {
  // 动画取消
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}

:deep(.el-tree-node__expand-icon.expanded:before) {
  // 收起
  content: "\e61a";
  font-size: 18px;
}

:deep(.el-tree-node__expand-icon:before) {
  // 展开
  content: "\e61b";
  font-size: 18px;
}


</style>