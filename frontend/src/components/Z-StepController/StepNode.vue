<template>
  <div class="step-node">
    <el-card class="step-card w100 h100"
             :class="[`${step.step_type}-border-color`]"
             :style="{borderColor: (node.isCurrent? getStepTypeInfo(step.step_type, 'color'):'')}"
    >
      <div class="step-header">

        <div class="step-header__index el-step__icon is-text el-tag--small"
             :style="{
          color: getStepTypeInfo(step.step_type, 'color'),
          backgroundColor: getStepTypeInfo(step.step_type, 'background')
        }"
        >
          <div class="el-step__icon-inner">{{ step.$index }}</div>
        </div>

        <div class="step-header__tag">
          <i :class="getStepTypeInfo(step.step_type, 'icon')"
             style="padding: 0 5px 0 5px; font-size: 18px"
             :style="{color: getStepTypeInfo(step.step_type, 'color')}"
          ></i>
        </div>
        <!--是否展开图标-->
        <div class="step-header__edit" v-if="step.step_type === 'loop'">
          <svg-icon v-show="shouDetailIcon(step.step_type)"
                    :name="step.showDetail ? 'ele-ArrowDown' : 'ele-ArrowRight'"
                    style="height: 20px; width: 20px">
          </svg-icon>
        </div>
        <!--脚本名称-->

        <div class="step-header__content">
          <template v-if="step.step_type === 'api'">
            <ApiHeader :data="step"/>
          </template>

          <template v-else-if="step.step_type === 'wait'">
            <WaitHeader :data="step"/>
          </template>

          <template v-else-if="step.step_type === 'if'">
            <IfControllerHeader :data="step"/>
          </template>

          <template v-else-if="step.step_type === 'loop'">
            <LoopHeader :data="step"/>
          </template>

          <template v-else>
            <span v-if="!step.edit && (step.step_type ==='sql' || step.step_type === 'script')">
              <span>{{ step.name }}</span>
              <svgIcon name="ele-EditPen"
                       @click.stop="editeName(step)"
                       style="margin-left: 5px; top:2px"></svgIcon>
            </span>
            <el-input v-else
                      :id="`editeName_${step.index}`"
                      v-model="step.name"
                      style="width: 200px;"
                      @click.stop.native=""
                      @blur="nameEditBlur(step)">
            </el-input>
            <!--            <span >{{ step.name }}</span>-->
          </template>
        </div>


        <!--              操作-->
        <div class="step-header__right header-right">
          <span @click.stop="">
            <el-tooltip content="启用/禁用" placement="top">
              <el-switch v-model="step.enable" inline-prompt>
              </el-switch>
            </el-tooltip>
          </span>

          <el-button circle style="margin-left: 5px" @click.stop="copyNode(step)">
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

      <div class="step-details" draggable="true" @dragstart="stepDetailsDrag">
        <ScriptHeader v-if="step.step_type === 'script'" :step="step"/>
        <SqlController v-if="step.step_type === 'sql'" :step="step"/>
        <!--        <ExtractController v-if="step.step_type === 'extract'" :extracts="step"/>-->
        <!--        <ApiInfoController v-if="data.step_type === 'api'" :data="data"/>-->
        <LoopController v-if="step.step_type === 'loop'" :step="step"/>
      </div>

    </el-card>
  </div>

</template>

<script setup name="StepNode">
import ScriptHeader from "/@/components/Z-StepController/script/ScriptHeader.vue";
import SqlController from "/@/components/Z-StepController/sql/SqlController.vue";
import WaitHeader from "/@/components/Z-StepController/wait/WaitHeader.vue";
import IfControllerHeader from "/@/components/Z-StepController/ifController/IfControllerHeader.vue";
import LoopHeader from "/@/components/Z-StepController/loop/LoopHeader.vue";
import LoopController from "/@/components/Z-StepController/loop/LoopController.vue";
import {getStepTypeInfo} from "/@/utils/case";
import ApiHeader from "/@/components/Z-StepController/apiInfo/ApiHeader.vue";
import useVModel from "/@/utils/useVModel";
import {nextTick} from "vue";

const emit = defineEmits(['copy-node', 'deleted-node'])

const props = defineProps({
  step: {
    type: Object,
    required: true
  },
  node: {
    type: Object,
    required: true
  },
  optType: {
    type: Object,
    required: true
  },
})

const step = useVModel(props, 'step', emit)

const editeName = (step) => {
  step.edit = true
  nextTick(() => {
    let inputRef = document.getElementById("editeName_" + step.index)
    if (inputRef) inputRef.focus();
  })
}

// 编辑失去焦点时触发
const nameEditBlur = (step) => {
  step.edit = false
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
const stepDetailsDrag = (event) => {
  event.stopPropagation();
  event.preventDefault()
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
      top: 5px;
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