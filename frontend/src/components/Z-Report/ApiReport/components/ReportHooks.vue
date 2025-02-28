<template>
  <el-row style="padding: 8px">
    <el-col :span="12" style="padding-right: 4px">
      <el-card>
        <template #header>
          前置hook
        </template>
        <el-collapse v-if="state.setupHookResults && state.setupHookResults.length > 0">
          <el-collapse-item v-for="(step, index) in state.setupHookResults" :key="step">
            <template #title>
              <div class="step-header">
                <div>
                  <div class="step-header__index el-step__icon is-text el-tag--small"
                       :style="{color: getStepTypeInfo(step.step_type, 'color'),backgroundColor: getStepTypeInfo(step.step_type, 'background')}">
                    <div class="el-step__icon-inner" style="font-size: 14px !important;">{{ index + 1 }}</div>
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
            <div v-if="step.step_type === 'sql'">
              {{ step.session_data?.sql }}
            </div>
            {{ step.message }}
          </el-collapse-item>
        </el-collapse>
      </el-card>
    </el-col>
    <el-col :span="12" style="padding-left: 4px">
      <el-card>
        <template #header>
          后置hook
        </template>
        <el-collapse v-if="state.teardownHookResults && state.teardownHookResults.length > 0">
          <el-collapse-item v-for="(step, index) in state.teardownHookResults" :key="step">
            <template #title>
              <div class="step-header">
                <div>
                  <div class="step-header__index el-step__icon is-text el-tag--small"
                       :style="{color: getStepTypeInfo(step.step_type, 'color'),backgroundColor: getStepTypeInfo(step.step_type, 'background')}">
                    <div class="el-step__icon-inner" style="font-size: 14px !important;">{{ index + 1 }}</div>
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
            <div v-if="step.step_type === 'sql'">
              {{ step.session_data?.sql }}
            </div>
            {{ step.message }}
          </el-collapse-item>
        </el-collapse>
      </el-card>

    </el-col>
  </el-row>
</template>

<script setup name="StepInfo">
import {getStepTypeInfo, stepTypes} from "/src/utils/case";
import {nextTick, onMounted, reactive, watch} from 'vue';

const props = defineProps({
  setupHookResults: {
    type: Array
  },
  teardownHookResults: {
    type: Array
  },
})

const state = reactive({
  setupHookResults: props.setupHookResults,
  teardownHookResults: props.teardownHookResults,

});

// 编辑脚本名称
const showDetail = (step) => {
  step.__edit = !step.__edit
}

watch(
    () => props.setupHookResults,
    () => {
      state.setupHookResults = props.setupHookResults
    },
    {deep: true}
)
watch(
    () => props.teardownHookResults,
    () => {
      state.teardownHookResults = props.teardownHookResults
    },
    {deep: true}
)

onMounted(() => {
  nextTick(() => {
    state.setupHookResults = props.setupHookResults
    state.teardownHookResults = props.teardownHookResults
  })
})

</script>

<style lang="scss" scoped>
.step-node {
  margin-top: 8px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 0 10px;

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