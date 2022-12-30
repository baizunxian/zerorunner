<template>
  <div class="step-node">
    <el-card class="step-card w100 h100"
             :style="{
          borderColor: (node.isCurrent? getStepTypeInfo(data.step_type, 'color'):''),
        }"
    >
      <div class="step-header">
        <!--步骤-->
        <div class="step-header__index el-step__icon is-text el-tag--small"
             :style="{
          color: getStepTypeInfo(data.step_type, 'color'),
          backgroundColor: getStepTypeInfo(data.step_type, 'background')
        }"
        >
          <div class="el-step__icon-inner">{{ data.index }}</div>
        </div>

        <!--        <svg-icon v-else name="ele-ArrowDown" style="height: 20px; width: 20px"></svg-icon>-->
        <div class="step-header__tag">
          <el-tag style="margin: 0 5px" size="small"
                  :style="{
          color: getStepTypeInfo(data.step_type, 'color'),
          backgroundColor: getStepTypeInfo(data.step_type, 'background')
        }"
          >
            {{ optType[data.step_type] }}
          </el-tag>
        </div>
        <!--是否展开图标-->
        <div class="step-header__edit">
          <svg-icon v-show="shouDetailIcon(data.step_type)"
                    :name="data.showDetail ? 'ele-ArrowDown' : 'ele-ArrowRight'"
                    style="height: 20px; width: 20px">
          </svg-icon>
        </div>
        <!--脚本名称-->
        <div class="step-header__content">
          <template v-if="data.step_type === 'wait'">
            <wait-header v-model:data="data"/>
          </template>

          <template v-else-if="data.step_type === 'if'">
            <condition-header v-model:data="data"/>
          </template>

          <template v-else-if="data.step_type === 'loop'">
            <loop-header v-model:data="data"/>
          </template>

          <template v-else>
          <span v-if="!data.edit">
            <i class="iconfont icon-drive_file"
               @click.stop="editeName(data)"
               style="margin-right: 5px">
            </i>
                {{ data.name }}
          </span>
            <el-input v-else
                      :id="`editeName_${data.index}`"
                      v-model="data.name"
                      style="width: 200px;"
                      @click.stop.native=""
                      @blur="nameEditBlur(data)">
            </el-input>
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

      <div class="step-details">
        <script-controller v-if="data.step_type === 'script'" v-model:data="data"/>
        <sql-controller v-if="data.step_type === 'sql'" v-model:data="data"/>
        <extract-controller v-if="data.step_type === 'extract'" v-model:data="data"/>
        <case-controller v-if="data.step_type === 'case'" v-model:data="data"/>
        <loop-controller v-if="data.step_type === 'loop'" v-model:data="data"/>
      </div>

    </el-card>
  </div>

</template>

<script lang="ts">
import {defineComponent, nextTick} from 'vue';
import scriptController from "/@/components/StepController/script/scriptController.vue";
import sqlController from "/@/components/StepController/sql/sqlController.vue";
import extractController from "/@/components/StepController/extract/extractController.vue";
import caseController from "/@/components/StepController/case/caseController.vue";
import waitHeader from "/@/components/StepController/wait/waitHeader.vue";
import conditionHeader from "/@/components/StepController/condition/conditionHeader.vue";
import loopHeader from "/@/components/StepController/loop/loopHeader.vue";
import loopController from "/@/components/StepController/loop/loopController.vue";
import {getStepTypeInfo} from "/@/utils/case";

export default defineComponent({
  name: 'stepNode',
  components: {
    scriptController,
    sqlController,
    extractController,
    caseController,
    waitHeader,
    conditionHeader,
    loopHeader,
    loopController,
  },
  props: {
    data: Object,
    node: Object,
    optType: Object,
  },
  emits: ['update:data', "copy-node", "deleted-node"],
  setup(props, {emit}) {
    // 编辑脚本名称
    const editeName = (data: any) => {
      data.edit = true
      nextTick(() => {
        let inputRef = document.getElementById("editeName_" + data.index)
        if (inputRef) inputRef.focus();
      })
    }

    // 编辑失去焦点时触发
    const nameEditBlur = (data: any) => {
      data.edit = false
    }

    const copyNode = (data: any) => {
      emit("copy-node", data)
    }

    const deletedNode = () => {
      emit("deleted-node")
    }

    // 是否展示展开图标
    const shouDetailIcon = (step_type: string) => {
      let noneType = ["wait", "if"]
      return noneType.indexOf(step_type) === -1
    }

    return {
      editeName,
      nameEditBlur,
      copyNode,
      deletedNode,
      getStepTypeInfo,
      shouDetailIcon,
    }
  },
});
</script>

<style lang="scss" scoped>
.step-node {
  margin: 0 0 0 0;
}

.step-card {
  min-height: 36px;

  .step-header {
    display: flex;
    min-height: 26px;
    padding: 0 10px;

    .el-tag--small {
      height: 24px;
    }

    .el-step__icon {
      top: 2px;
      width: 20px;
      height: 20px;
      font-size: 12px;
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
</style>