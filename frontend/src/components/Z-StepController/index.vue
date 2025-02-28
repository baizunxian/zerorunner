<template>
  <div class="h100" id="stepController" style="overflow-y: auto">
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
          :props="{children: 'children_steps'}"
          :data="steps">
        <template #default="{ node }">
          <StepNode v-model:step="node.data"
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

    <SelectCase ref="selectApiRef" @addApiStep="addApiStep"></SelectCase>
    <ApiInfoController ref="ApiInfoControllerRef"></ApiInfoController>

  </div>
</template>

<script setup name="stepController">
import {reactive, ref, watch} from 'vue';
import StepNode from "/@/components/Z-StepController/StepNode.vue";
import SelectCase from "/@/components/Z-StepController/apiInfo/SelectApi.vue";
import ApiInfoController from "./apiInfo/ApiInfoController.vue"
import useVModel from "/@/utils/useVModel";
import {useApiInfoApi} from "/@/api/useAutoApi/apiInfo";

const emit = defineEmits(['update:steps'])
const props = defineProps({
  use_type: {
    type: String,
    default: () => {
      return 'pre'   // pre 前置  post 候置  case 用例
    }
  },
  steps: {
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

const steps = useVModel(props, 'steps', emit)


const ApiInfoControllerRef = ref()
const selectApiRef = ref()
const stepTreeRef = ref()

const state = reactive({
  // data
  optType: "script",
  optTypes: {},
  // caseInfo
  showApioInfo: false,

});

// 拖动处理
const allowDrop = (draggingNode, dropNode, type) => {
  if (dropNode.data.step_type === 'if' && type === 'inner') {
    return true
  } else if (dropNode.data.step_type === 'loop' && type === 'inner') {
    return true
  }
  // return type
  return type !== "inner"
}

// 节点拖动完成重新计算顺序
const handleDrop = (node, event) => {
  // event.preventDefault()
  // event.stopPropagation()
  // return false
}

const nodeClick = (data, node) => {
  if (data.step_type === "api") {
    ApiInfoControllerRef.value.onOpenApiInfoPage(data)
  } else {
    data.showDetail = !data.showDetail
  }
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data, parent_index = 0) => {
  if (data) {
    data.forEach((e, index) => {
      e.$index = index + 1
      e.index = index
      if (e.children_steps) {
        computeDataIndex(e.children_steps, parent_index)
      } else {
        e.children_steps = []
      }
    })
  }
}
// handleAddData
const handleAddData = async (optType) => {
  if (optType !== 'api') {
    let stepData = getAddData(optType)
    appendTreeDate(stepData)
  } else {
    selectApiRef.value.onOpenApiList()
  }
}

// 添加tree data
const appendTreeDate = (data) => {
  let parentNode = stepTreeRef.value?.getCurrentNode()
  if (parentNode && props.use_type === "case") {
    if (!parentNode.children_steps) {
      parentNode.children_steps = []
    }
    stepTreeRef.value.append(data, parentNode.id)
  } else {
    stepTreeRef.value.append(data, null)
  }
}

const getStepData = () => {
  return {
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
    showDetail: false,
    is_quotation: true,
    children_step: []
  }
}

// 获取步骤
const getAddData = (optType) => {
  let data = getStepData()
  data.name = `${optType}_${getRandomStr()}`
  data.step_type = optType
  if (optType === "script") {
    data.name = "自定义脚本"
    data.request = {
      script_content: ""
    }
  } else if (optType === "sql") {
    data.name = "数据库操作"
    data.request = {
      env_id: null,
      source_id: null,
      sql: "",
      timeout: 0,
      variable_name: ""
    }
  } else if (optType === "wait") {
    data.request = {
      wait_time: 0
    }

  } else if (optType === "if") {
    data.request = {
      check: "",
      comparator: "",
      expect: "",
      remarks: ""
    }
  } else if (optType === "loop") {
    data.request = {
      // loop_type = count
      loop_type: "count",
      count_number: 0,
      count_sleep_time: 0,

      // loop_type == "for"
      for_variable_name: "",
      for_variable: "",
      for_sleep_time: 0,

      // loop_type == "while"
      while_comparator: "",
      while_variable: "",
      while_value: "",
      while_sleep_time: 0,
      while_timeout: 0
    }
  } else if (optType === "api") {
    selectApiRef.value.onOpenApiList()
  }
  return data
}

// 添加case
const addApiStep = async () => {
  let selectApiData = selectApiRef.value.getSelectionData()
  if (selectApiData) {
    let apiIds = selectApiData.map(e => {
      return e.id
    })
    let {data} = await useApiInfoApi().getApiInfos({ids: apiIds})
    if (data && data.length > 0) {
      data.forEach(apiInfo => {
        let stepData = Object.assign({}, apiInfo)
        stepData.id = null
        stepData.step_type = "api"
        stepData.source_id = apiInfo.id
        stepData.enable = true
        appendTreeDate(stepData)
      })
    }

  }
  state.showApioInfo = false
}

const getRandomStr = () => {
  return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
}

const deletedNode = (node) => {
  stepTreeRef.value.remove(node)
  // props.data.splice(index, 1)
}
const copyNode = (data) => {
  data = JSON.parse(JSON.stringify(data))
  steps.value.push(data)
}

watch(
    () => steps.value,
    (value) => {
      console.log(1111)
      computeDataIndex(steps.value)
    },
    {deep: true}
)

defineExpose({
  handleAddData,
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

:deep(.el-tree-node__expand-icon.is-leaf) {
  color: transparent;
  cursor: default;
}

:deep(.el-tree-node__expand-icon) {
  // 更换图标库
  font-family: "iconfont" !important;
  color: #1f1f1f;

  svg {
    display: none;
  }

  font-style: normal;
}

</style>