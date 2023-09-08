<template>
  <div class="h100" id="stepController" style="overflow-y: auto">
    <el-backtop :right="200" :bottom="200" :visibility-height="10" target="#stepController"/>
    <div class="h100" style="overflow-y: auto;">
      <!--      <el-dropdown style="padding-left: 33px">-->
      <!--        <el-button type="primary">-->
      <!--          {{ `添加${use_type === 'case' ? '步骤' : 'Hook'}` }}-->
      <!--          <el-icon class="el-icon&#45;&#45;right">-->
      <!--            <arrowDown/>-->
      <!--          </el-icon>-->
      <!--        </el-button>-->
      <!--        <template #dropdown>-->
      <!--          <el-dropdown-menu>-->
      <!--            <el-dropdown-item v-for="(value, key)  in state.optTypes"-->
      <!--                              :key="key"-->
      <!--                              style="margin: 5px 0"-->
      <!--                              :style="{ color: getStepTypeInfo(key,'color')}"-->
      <!--                              @click="handleAddData(key)">-->
      <!--              <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"-->
      <!--                 :style="{color:getStepTypeInfo(key,'color')}"></i>-->
      <!--              {{ value }}-->
      <!--            </el-dropdown-item>-->

      <!--          </el-dropdown-menu>-->
      <!--        </template>-->
      <!--      </el-dropdown>-->

      <el-tree
          ref="stepTreeRef"
          draggable
          highlight-current
          :allow-drop="allowDrop"
          @node-click="nodeClick"
          node-key="id"
          @node-drag-start="handleDrop"
          :expand-on-click-node="false"
          :props="{children: 'sub_steps'}"
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

    <SelectCase ref="selectApiRef" @addApiStep="addApiStep"></SelectCase>
    <ApiInfoController ref="ApiInfoControllerRef"></ApiInfoController>

  </div>
</template>

<script lang="ts" setup name="stepController">
import type {PropType} from 'vue'
import {nextTick, onMounted, reactive, ref, watch} from 'vue';
import {useRoute, useRouter} from "vue-router"
import StepNode from "/@/components/Z-StepController/StepNode.vue";
import SelectCase from "/@/components/Z-StepController/apiInfo/SelectApi.vue";
import {getStepTypeInfo, getStepTypesByUse} from "/@/utils/case";
import {ArrowDown} from '@element-plus/icons-vue'
import ApiInfoController from "./apiInfo/ApiInfoController.vue"


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
    type: [Number, String, null] as PropType<Number | String | null>,
    default: () => {
      return null
    }
  }
})

const ApiInfoControllerRef = ref()
const route = useRoute()
const router = useRouter()
const selectApiRef = ref()
const stepTreeRef = ref()

const state = reactive({
  // data
  optType: "script",
  optTypes: {},
  // caseInfo
  showApioInfo: false,

});


const initFabMenu = (stepType: string | null) => {
  state.optTypes = getStepTypesByUse(props.use_type)
}

// 拖动处理
const allowDrop = (draggingNode: any, dropNode: any, type: any) => {
  if (dropNode.data.step_type === 'if' && type === 'inner') {
    return true
  } else if (dropNode.data.step_type === 'loop' && type === 'inner') {
    return true
  }
  // return type
  return type !== "inner"
}

// 节点拖动完成重新计算顺序
const handleDrop = (node: any, event: any) => {
  // return false
}

const nodeClick = (data: any, node: any) => {
  if (data.step_type == "api") {
    ApiInfoControllerRef.value.onOpenApiInfoPage(data)
  } else {
    data.showDetail = !data.showDetail
  }
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data: any) => {
  if (data) {
    data.forEach((data: any, index: number) => {
      data.index = index + 1
      if (data.sub_steps) {
        computeDataIndex(data.sub_steps)
      }
    })
  }
}
// handleAddData
const handleAddData = async (optType: string) => {
  if (optType !== 'api') {
    let stepData = await getAddData(optType)
    appendTreeDate(stepData)
  } else {
    selectApiRef.value.onOpenApiList()
  }
}

// 添加tree data
const appendTreeDate = (data: any) => {
  let parentNode = stepTreeRef.value?.getCurrentNode()
  if (parentNode && props.use_type === "case") {
    if (!parentNode.sub_steps) {
      parentNode.sub_steps = []
    }
    // parentNode.teststeps.push(data)
    // emit("update:data", [...props.data])
    // props.data = [...props.data]
    stepTreeRef.value.append(data, parentNode.id)
  } else {
    // props.data.push(data)
    stepTreeRef.value.append(data, null)
  }
}

const getStepData = () => {
  let stepData: TStepDataStat = {
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
    showDetail: false,
  }
  return stepData
}

// 获取步骤
const getAddData = (optType: string) => {
  let data = getStepData()
  data.name = `${optType}_${getRandomStr()}`
  data.step_type = optType
  if (optType === "script") {
    data.script_request = {
      script_content: ""
    }
  } else if (optType === "sql") {
    data.sql_request = {
      env_id: null,
      source_id: null,
      sql: "",
      timeout: 0,
      variable_name: ""
    }
  } else if (optType === "wait") {
    data.wait_request = {
      wait_time: 0
    }

  }
      // else if (optType === "extract") {
      //   data = {
      //     id: id,
      //     name: name,
      //     value: null,
      //     json_path_list: [],
      //     step_type: "extract",
      //     enable: true
      //   }
  // }
  else if (optType === "if") {
    data.if_request = {
      check: "",
      comparator: "",
      expect: "",
      remarks: ""
    }
  } else if (optType === "loop") {
    data.loop_request = {
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
const addApiStep = () => {
  let selectApiData = selectApiRef.value.getSelectionData()
  if (selectApiData) {
    selectApiData.forEach((apiInfo: any) => {
      // if (state.optType === "case" && caseInfo.id === parseInt(props.case_id)) {
      //   ElMessage.warning('不能引用用例自己！');
      // } else {
      let stepData = getStepData()
      stepData.step_type = "api"
      stepData.name = apiInfo.name
      stepData.request = {
        name: apiInfo.name,
        api_id: apiInfo.id,
        method: apiInfo.method
      }
      appendTreeDate(stepData)
      // }
    })
  }
  state.showApioInfo = false
}

const getRandomStr = () => {
  return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
}

const deletedNode = (node: any) => {
  stepTreeRef.value.remove(node)
  // props.data.splice(index, 1)
}
const copyNode = (data: any) => {
  props.data.push(JSON.parse(JSON.stringify(data)))
}

const clickBlank = () => {
  stepTreeRef.value?.setCurrentKey(null)
}

watch(
    () => props.data,
    (value) => {
      computeDataIndex(value)
    },
    {
      deep: true
    }
)

onMounted(() => {
  initFabMenu(null)
})

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