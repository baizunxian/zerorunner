<template>
  <div>
    <el-collapse>
      <el-collapse-item v-for="(step, index) in stepData" :key="step">
        <template #title>
          <div class="step-header">
            <div>
              <div class="step-header__index el-step__icon is-text el-tag--small"
                   :style="{color: getStepTypeInfo(step.step_type, 'color'),backgroundColor: getStepTypeInfo(step.step_type, 'background')}">
                <div class="el-step__icon-inner">{{ index + 1 }}</div>
              </div>
              <el-tag style="margin: 0 5px" size="small"
                      :style="{color: getStepTypeInfo(step.step_type, 'color'),backgroundColor: getStepTypeInfo(step.step_type, 'background')}">
                {{ stepTypes[step.step_type] }}
              </el-tag>
            </div>

            <div>
              <div style="font-size: 12px;">
                <span v-if="step.status === 'success'"
                      style="margin-right: 20px; color: var(--el-color-success)">{{ step.status }}</span>
                <span v-if="step.status === 'fail'"
                      style="margin-right: 20px; color: var(--el-color-warning)">{{ step.status }}</span>
                <span v-if="step.status === 'err'"
                      style="margin-right: 20px; color: var(--el-color-danger)">{{ step.status }}</span>
                <el-tag :type="step.success? 'success': 'danger'">{{ step.success ? "通过" : "不通过" }}
                </el-tag>
              </div>

            </div>

          </div>

        </template>
        {{ step.message }}
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts">
import {getStepTypeInfo, stepTypes} from "/@/utils/case";
import {defineComponent, nextTick, onMounted, PropType, reactive, watch, toRefs} from 'vue';
import {StepData} from "/@/components/Report/ApiReport/apiReport";


export default defineComponent({
  name: 'stepNode',
  components: {},
  props: {
    data: {type: Array as PropType<Array<StepData>>},
  },
  emits: ['update:data', "copy-node", "deleted-node"],
  setup(props) {
    const state = reactive({
      // data
      stepData: props.data

    });

    // 编辑脚本名称
    const showDetail = (step: any) => {
      step.__edit = !step.__edit
    }

    watch(
        () => props.data,
        () => {
          state.stepData = props.data
        },
        {deep: true}
    )

    onMounted(() => {
      nextTick(() => {
        state.stepData = props.data
      })
    })


    return {
      stepTypes,
      showDetail,
      getStepTypeInfo,
      ...toRefs(state)
    }
  },
});
</script>

<style lang="scss" scoped>
.step-node {
  margin-top: 8px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  width: 100%;

  .el-tag--small {
    height: 24px;
  }

  .el-step__icon {
    //top: 2px;
    width: 20px;
    height: 20px;
    font-size: 12px;
  }
}

.el-step__icon.is-text {
  border: 1px solid;
}

:deep(.el-tag) {
  border-color: #e4d7e7;
}
</style>