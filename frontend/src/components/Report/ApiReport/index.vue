<template>
  <div class="system-edit-menu-container h100">
    <div style="height:100%; overflow-y: auto">
      <el-tree
          draggable
          :allow-drop="allowDrop"
          @node-drop="handleDrop"
          @node-click="nodeClick"
          :props="{children: 'step_datas', label:'name' }"
          :data="data">
        <template #default="{ node }">
          <report-node v-model:data="node.data"/>
        </template>
      </el-tree>
    </div>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue';
import {useRoute, useRouter} from "vue-router"
import reportNode from "/@/components/Report/ApiReport/reportNode.vue";

export default defineComponent({
  name: 'apiReport',
  components: {
    reportNode,
  },
  props: {
    data: {
      type: Array,
      default: () => []
    },
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

    const initData = () => {
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

    const getRandomStr = () => {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
    }

    onMounted(() => {
      initData()
    })

    return {
      allowDrop,
      handleDrop,
      nodeClick,
      route,
      router,
      getRandomStr,
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