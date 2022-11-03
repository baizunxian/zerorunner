<template>
  <div class="system-edit-menu-container h100">
    <el-row :span="24" style="padding-left: 25px">
      <el-col :span="3">
        <el-select size="small"
                   v-model="optType"
                   placeholder=""
                   filterable
                   class="w100">
          <el-option
              v-for="(value, key) in optTypes"
              :key="key"
              :label="value"
              :value="key">
          </el-option>
        </el-select>
      </el-col>

      <el-col :span="1" style="padding-left: 5px">
        <el-button @click="addStep" type="primary">添加</el-button>
      </el-col>

    </el-row>

    <div style="height:100%; overflow-y: auto">
      <el-tree
          draggable
          :allow-drop="allowDrop"
          @node-drop="handleDrop"
          @node-click="nodeClick"
          :data="data">
        <template #default="{ node }">
          <step-node v-model:data="node.data"
                     :opt-type="optTypes"
                     @copy-node="copyNode"
                     @deleted-node="deletedNode"
          />
        </template>
      </el-tree>
    </div>

    <el-dialog
        draggable
        title="用例引用"
        v-model="showCaseInfo"
        width="60%">
      <select-case ref="selectCaseRef"></select-case>
      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addCaseStep">引用</el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue';
import type {PropType} from 'vue'
import {useRoute, useRouter} from "vue-router"
import stepNode from "/@/components/StepController/stepNode.vue";
import selectCase from "/@/components/StepController/selectCase.vue";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: 'stepController',
  components: {
    stepNode,
    selectCase,
  },
  props: {
    step_type: {
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
  },
  setup(props: any) {
    const route = useRoute()
    const router = useRouter()
    const selectCaseRef = ref()
    const state = reactive({
      // data
      optType: "script",
      optTypes: {},
      // caseInfo
      showCaseInfo: false,

    });

    const initController = () => {
      switch (props.step_type) {
        case "pre":
          state.optTypes = {
            script: "前置脚本",
            sql: "前置SQL",
            wait: "等待控制器",
            case: "用例引用",
          }
          break
        case "post":
          state.optTypes = {
            script: "后置脚本",
            sql: "后置SQL",
            extract: "提取参数",
          }
          break
        case "suite":
          state.optTypes = {
            case: "用例引用",
            script: "自定义脚本",
            sql: "SQL控制器",
            wait: "等待控制器",
          }
          state.optType = "case"
          break
        default:
          break
      }
    }


    // 不允许拖动为子
    const allowDrop = (draggingNode: any, dropNode: any, type: any) => {
      return type !== "inner"
    }

    // 节点拖动完成重新计算顺序
    const handleDrop = () => {
      computeDataIndex()
    }

    const nodeClick = (data: any) => {
      data.showDetail = !data.showDetail
    }

    // 计算index，保持拖动后顺序
    const computeDataIndex = () => {
      props.data.forEach((data: any, index: number) => {
        data.index = index + 1
      })
    }
    // 追加步骤
    const addStep = () => {
      let data = null
      if (state.optType === "script") {
        data = {name: `script_${getRandomStr()}`, value: "", step_type: "script", enable: true}
      } else if (state.optType === "sql") {
        data = {
          name: `sql_${getRandomStr()}`,
          value: "",
          step_type: "sql",
          timeout: null,
          variable_name: "",
          enable: true
        }
      } else if (state.optType === "wait") {
        data = {name: `wait_${getRandomStr()}`, value: null, step_type: "wait", enable: true}
      } else if (state.optType === "extract") {
        data = {name: `extract_${getRandomStr()}`, value: null, json_path_list: [], step_type: "extract", enable: true}
      } else if (state.optType === "case") {
        state.showCaseInfo = true
        // data = {name: "", value: null, step_type: "apiCase", enable: true}
      }
      if (data) props.data.push(data)
      computeDataIndex()
    }

    const addCaseStep = () => {
      let selectCaseData = selectCaseRef.value.getSelectionData()
      if (selectCaseData) {
        selectCaseData.forEach((caseInfo: any) => {
          if (state.optType === "case" && caseInfo.id === parseInt(props.case_id)) {
            ElMessage.warning('不能引用用例自己！');
          } else {
            let stepData = {name: caseInfo.name, value: caseInfo.id, step_type: "case", enable: true}
            props.data.push(stepData)
          }
        })
      }
      state.showCaseInfo = false
      computeDataIndex()
    }

    const getRandomStr = () => {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
    }

    const deletedNode = (index: number) => {
      props.data.splice(index, 1)
      computeDataIndex()
    }
    const copyNode = (data: any) => {
      props.data.push(JSON.parse(JSON.stringify(data)))
      computeDataIndex()
    }


    onMounted(() => {
      initController()
    })


    return {
      allowDrop,
      handleDrop,
      nodeClick,
      addStep,
      route,
      router,
      addCaseStep,
      getRandomStr,
      deletedNode,
      copyNode,
      selectCaseRef,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

// el-terr
:deep(.el-tree-node__content) {
  height: 100%;
  //max-height: 26px;
  margin-top: 6px;
  vertical-align: center;
  -webkit-box-align: center;
  display: flex;
  cursor: pointer;
  align-items: center;
}

:deep(.el-card__body) {
  padding: 5px 10px;
}

:deep(.el-tree-node__label) {
  width: 100%;
}
</style>