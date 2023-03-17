<template>
  <div class="h100" id="stepController" style="overflow-y: auto">
    <el-backtop :right="200" :bottom="200" :visibility-height="10" target="#stepController"/>

    <FabButton v-if="use_type==='suite'" :value="state.suiteOpt"></FabButton>
    <el-row :span="24" style="padding-left: 25px" v-else>
      <el-col :span="3">
        <el-select size="small"
                   v-model="state.optType"
                   placeholder=""
                   filterable
                   class="w100">
          <el-option
              v-for="(value, key) in state.optTypes"
              :key="key"
              :label="value"
              :value="key">
            <!--            <el-tag size="small">{{ value }}</el-tag>-->
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="1" style="padding-left: 5px">
        <el-button @click="handleAddData(state.optType)" type="primary">添加</el-button>
      </el-col>
    </el-row>

    <div class="h100" style="overflow-y: auto;">
      <el-tree
          ref="stepTreeRef"
          draggable
          highlight-current
          :allow-drop="allowDrop"
          @node-drop="handleDrop"
          @node-click="nodeClick"
          node-key="id"
          :expand-on-click-node="false"
          :props="{children: 'teststeps'}"
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

    <el-dialog
        draggable
        title="添加接口"
        v-model="state.showApioInfo"
        width="60%">
      <SelectCase ref="selectCaseRef"></SelectCase>
      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addApiStep">添加</el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script lang="ts" setup name="stepController">
import type {PropType} from 'vue'
import {nextTick, onMounted, reactive, ref, watch, Directive, DirectiveBinding} from 'vue';
import {useRoute, useRouter} from "vue-router"
import StepNode from "/@/components/Z-StepController/StepNode.vue";
import SelectCase from "/@/components/Z-StepController/apiInfo/SelectApi.vue";
import FabButton from "/@/components/fabButton/index.vue";
import {getStepTypeInfo, getStepTypesByUse} from "/@/utils/case";
// import {ClickOutside as vClickOutside} from "element-plus";



const emit = defineEmits([])

const props = defineProps({
  use_type: {
    type: String,
    default: () => {
      return 'pre'   // pre 前置  post 候置  suite 套件
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


const route = useRoute()
const router = useRouter()
const selectCaseRef = ref()
const stepTreeRef = ref()
const state = reactive({
  // data
  optType: "script",
  optTypes: {},
  // caseInfo
  showApioInfo: false,
  // suite opt
  suiteOpt: [],
  id: 1000,

});


const initFabMenu = (stepType: string | null) => {
  state.optTypes = getStepTypesByUse(props.use_type)
  let noMenuTypes = ["wait", "script", "api", "case"]
  if (props.use_type == 'suite' && (stepType === null || noMenuTypes.indexOf(stepType) === -1)) {
    let suiteOptList: any = []
    for (let optTypesKey in state.optTypes) {
      let color: string = getStepTypeInfo(optTypesKey, "color")
      let icon: string = getStepTypeInfo(optTypesKey, "icon")
      let suiteOptData: any = {
        title: state.optTypes[optTypesKey],
        func: handleAddData,
        param: optTypesKey,
        color: color,
        icon: icon,
      }
      suiteOptList.push(suiteOptData)
    }
    state.suiteOpt = suiteOptList
  } else {
    state.suiteOpt = []
  }

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
const handleDrop = () => {
  // computeDataIndex()
}

const nodeClick = (data: any, node: any) => {
  console.log("node----->", node)
  data.showDetail = !data.showDetail
  initFabMenu(data.step_type)
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data: any) => {
  data.forEach((data: any, index: number) => {
    data.index = index + 1
    // if (!data.id) {
    //   data.id = state.id++
    // }
    if (data.teststeps) {
      computeDataIndex(data.teststeps)
    }
  })
}
// handleAddData
const handleAddData = async (optType: string) => {
  if (optType !== 'api') {
    let stepData = await getAddData(optType)
    appendTreeDate(stepData)
  } else {
    state.showApioInfo = true
  }
}

// 添加tree data
const appendTreeDate = (data: any) => {
  let parentNode = stepTreeRef.value?.getCurrentNode()
  if (parentNode && props.use_type === "suite") {
    if (!parentNode.teststeps) {
      parentNode.teststeps = []
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

// 获取步骤
const getAddData = (optType: string) => {
  let id = state.id++
  let data = null
  let name = `${optType}_${getRandomStr()}`
  if (optType === "script") {
    data = {
      id: id,
      name: name,
      value: "",
      step_type: optType,
      enable: true
    }
  } else if (optType === "sql") {
    data = {
      id: id,
      name: name,
      value: "",
      step_type: optType,
      timeout: null,
      variable_name: "",
      enable: true
    }
  } else if (optType === "wait") {
    data = {
      id: id,
      name: name,
      value: null,
      step_type: "wait",
      enable: true
    }
  } else if (optType === "extract") {
    data = {
      id: id,
      name: name,
      value: null,
      json_path_list: [],
      step_type: "extract",
      enable: true
    }
  } else if (optType === "if") {
    data = {
      id: id,
      name: name,
      value: null,
      comparator: "",
      remarks: "",
      step_type: optType,
      enable: true
    }
  } else if (optType === "loop") {
    data = {
      id: id,
      name: name,
      step_type: optType,
      loop_type: "count",
      count_number: 0,
      enable: true
    }
  } else if (optType === "api") {
    state.showApioInfo = true
  }
  return data
}

// 添加case
const addApiStep = () => {
  let selectCaseData = selectCaseRef.value.getSelectionData()
  if (selectCaseData) {
    selectCaseData.forEach((caseInfo: any) => {
      // if (state.optType === "case" && caseInfo.id === parseInt(props.case_id)) {
      //   ElMessage.warning('不能引用用例自己！');
      // } else {
      let stepData = {id: state.id++, name: caseInfo.name, case_id: caseInfo.id, step_type: "api", enable: true}
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

const onClickOutside = () => {
  console.log("1111")
  clickBlank()
  initFabMenu(null)
}


// tree 自定义内容 引用组件导致宽度丢失问题
// const setStyle = () => {
//   let caseStepElList: any = document.getElementsByClassName("treeCaseStep")
//   if (caseStepElList && caseStepElList.length > 0) {
//     for (let i = 0; i <= caseStepElList.length; i++) {
//       if (caseStepElList[i]) caseStepElList[i].parentNode.style.width = "calc(100% - 24px)"
//     }
//   }
// }

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
  nextTick(() => {
    // setStyle()
  })
})

defineExpose({
  clickBlank,
  initFabMenu,
})

</script>

<style lang="scss" scoped>

// el-terr
:deep(.el-tree-node__content) {
  height: 100%;
  margin-top: 6px;
  vertical-align: center;
  display: flex;
  cursor: pointer;
  align-items: center;
}

//:deep(.el-card__body) {
//  padding: 5px 10px;
//}

:deep(.el-tree-node__label) {
  width: 100%;
}

:deep(.el-input--small .el-input__inner) {
  --el-input-inner-height: calc(var(--el-input-height, 24px) - 1px);
}
</style>


<style lang="scss" scoped>
// el-tree 展开图标修改

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