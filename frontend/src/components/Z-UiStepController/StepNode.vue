<template>
  <div class="step-node">
    <el-card class="step-card w100 h100"
             :class="[`${data.step_type}-border-color`]"

    >
      <div class="step-header">

<!--        <div class="step-header__tag">-->
<!--          <i :class="getStepTypeInfo(data.step_type, 'icon')"-->
<!--             style="padding: 0 5px 0 5px; font-size: 18px"-->
<!--             :style="{color: getStepTypeInfo(data.step_type, 'color')}"-->
<!--          ></i>-->
<!--        </div>-->
        <!--是否展开图标-->
        <div class="step-header__edit" v-if="data.step_type === 'loop'">
          <svg-icon v-show="shouDetailIcon(data.step_type)"
                    :name="data.showDetail ? 'ele-ArrowDown' : 'ele-ArrowRight'"
                    style="height: 20px; width: 20px">
          </svg-icon>
        </div>
        <!--脚本名称-->
        <div class="step-header__content">
          <template v-if="data.step_type === 'api'">
            <ApiHeader :data="data"/>
          </template>

          <template v-else-if="data.step_type === 'wait'">
            <WaitHeader :data="data"/>
          </template>

          <template v-else-if="data.step_type === 'if'">
            <IfControllerHeader :data="data"/>
          </template>

          <template v-else-if="data.step_type === 'loop'">
            <LoopHeader :data="data"/>
          </template>

          <template v-else>
            <span>{{ data.name }}</span>
          </template>
        </div>

        <!--              操作-->
        <div class="step-header__right header-right">
          <span @click.stop="">
            <el-tooltip content="启用/禁用" placement="top">
              <el-switch
                  v-model="data.enable"
                  inline-prompt>
              </el-switch>
            </el-tooltip>
          </span>

          <el-button circle style="margin-left: 5px" @click.stop="copyNode(data)">
            <el-icon>
              <ele-DocumentCopy/>
            </el-icon>
          </el-button>

          <el-button type="danger" circle @click.stop="deletedNode">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </div>
      </div>

<!--      <div class="step-details">-->
<!--        <ScriptController v-if="data.step_type === 'script'" :data="data"/>-->
<!--        <SqlController v-if="data.step_type === 'sql'" :data="data"/>-->
<!--        <ExtractController v-if="data.step_type === 'extract'" :data="data"/>-->
<!--        &lt;!&ndash;        <ApiInfoController v-if="data.step_type === 'api'" :data="data"/>&ndash;&gt;-->
<!--        <LoopController v-if="data.step_type === 'loop'" :data="data"/>-->
<!--      </div>-->

    </el-card>
  </div>

</template>

<script setup name="StepNode">
import {nextTick} from 'vue';
import WaitHeader from "/@/components/Z-StepController/wait/WaitHeader.vue";
import IfControllerHeader from "/@/components/Z-StepController/ifController/IfControllerHeader.vue";
import LoopHeader from "/@/components/Z-StepController/loop/LoopHeader.vue";
import ApiHeader from "/@/components/Z-StepController/apiInfo/ApiHeader.vue";

const emit = defineEmits(['copy-node', 'deleted-node'])

const props = defineProps({
  data: {
    type: Object,
  },
  node: {
    type: Object,
  },
  optType: {
    type: Object,
  },
})

const editeName = (data) => {
  data.edit = true
  nextTick(() => {
    let inputRef = document.getElementById("editeName_" + data.index)
    if (inputRef) inputRef.focus();
  })
}

// 编辑失去焦点时触发
const nameEditBlur = (data) => {
  data.edit = false
}

const copyNode = (data) => {
  emit("copy-node", data)
}

const deletedNode = () => {
  emit("deleted-node")
}

// 是否展示展开图标
const shouDetailIcon = (step_type) => {
  let noneType = ["wait", "if"]
  return noneType.indexOf(step_type) === -1
}

</script>

<style lang="scss" scoped>
.script-border-color:hover {
  border-color: #7B4D12FF
}

.wait-border-color:hover {
  border-color: #67C23AFF
}

.api-border-color:hover {
  border-color: #61649f
}

.case-border-color:hover {
  border-color: #61649f
}

.loop-border-color:hover {
  border-color: #02A7F0FF
}

.extract-border-color:hover {
  border-color: #015478FF
}

.sql-border-color:hover {
  border-color: #783887FF
}

.if-border-color:hover {
  border-color: #E6A23C
}


.step-node {
  margin: 0 0 0 0;
  width: 100%;
  //height: 48px;

  :deep(.el-card__body) {
    height: 100%;
  }
}

.step-card {
  //padding: 8px !important;
  min-height: 36px;

  :deep(.el-card__body) {
    padding: 8px 0 !important;
  }

  .step-header {
    display: flex;
    height: 30px;
    line-height: 30px;
    padding: 0 10px;

    .el-tag--small {
      height: 24px;
    }

    .el-step__icon {
      top: 2px;
      width: 20px;
      height: 20px;
    }

    .el-step__icon-inner {
      font-size: 12px !important;
    }

    .step-header__content {
      width: 100%;
    }

    .step-header__right {
      //margin-top: 1px;
      //float: right;
      //z-index: 1;
      margin-left: auto;
    }

  }

  .step-details {
    //width: 100%;
  }
}

.el-step__icon.is-text {
  border: 1px solid;
}

:deep(.el-tag) {
  border-color: #e4d7e7;
}

:deep(.el-card) {
  border-radius: 6px;
}
</style>