<template>
  <div class="case-tabs" style="padding: 10px">
    <el-row>
      <el-col :span="12" style="padding: 0 10px">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>前置 Hook</span>
              <el-dropdown style="padding-left: 33px">
                <el-button type="success" plain round >
                  添加Hook
                  <el-icon class="el-icon--right">
                    <arrowDown/>
                  </el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item v-for="(value, key)  in state.optTypes"
                                      :key="key"
                                      style="margin: 5px 0"
                                      :style="{ color: getStepTypeInfo(key,'color')}"
                                      @click="handleAddData('setup', key)">
                      <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"
                         :style="{color:getStepTypeInfo(key,'color')}"></i>
                      {{ value }}
                    </el-dropdown-item>

                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>

          </template>
          <div class="step-details">
            <z-step-controller ref="setupHooksRef"
                               use_type="pre"
                               :steps="state.setup_hooks"
                               :case_id="state.case_id">
            </z-step-controller>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12" style="padding: 0 10px">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>后置 Hook</span>
              <el-dropdown style="padding-left: 33px">
                <el-button type="success" plain round >
                  添加Hook
                  <el-icon class="el-icon--right">
                    <arrowDown/>
                  </el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item v-for="(value, key)  in state.optTypes"
                                      :key="key"
                                      style="margin: 5px 0"
                                      :style="{ color: getStepTypeInfo(key,'color')}"
                                      @click="handleAddData('teardown', key)">
                      <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"
                         :style="{color:getStepTypeInfo(key,'color')}"></i>
                      {{ value }}
                    </el-dropdown-item>

                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
          <div class="step-details">
            <z-step-controller ref="teardownHookRef"
                               use_type="post"
                               :steps="state.teardown_hooks"
                               :case_id="state.case_id">
            </z-step-controller>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="preOperation">
import {reactive, ref} from 'vue';
import {handleEmpty} from "/@/utils/other";
import {ArrowDown} from "@element-plus/icons";
import {getStepTypesByUse, getStepTypeInfo} from "/@/utils/case";

const setupHooksRef = ref()
const teardownHookRef = ref()

const state = reactive({
  setup_hooks: [],
  teardown_hooks: [],
  case_id: 0,
  optTypes: getStepTypesByUse("hook"),
});

// init hook
const setData = (setup_hooks, teardown_hooks, case_id) => {
  state.setup_hooks = setup_hooks ? setup_hooks : []
  state.teardown_hooks = teardown_hooks ? teardown_hooks : []
  state.case_id = case_id ? case_id : 0
}

const getDataLength = () => {
  return state.setup_hooks.length + state.teardown_hooks.length
}

// 获取表单数据
const getData = () => {
  return {
    setup_hooks: handleEmpty(state.setup_hooks),
    teardown_hooks: handleEmpty(state.teardown_hooks)
  }
}

const handleAddData = (hook_type, optType) => {
  if (hook_type === "setup") {
    setupHooksRef.value.handleAddData(optType)
  } else if (hook_type === "teardown") {
    teardownHookRef.value.handleAddData(optType)
  }
}

defineExpose({
  setData,
  getData,
  getDataLength,
})

</script>

<style lang="scss" scoped>

:deep(.el-card__body) {
  padding: 8px 0 !important;
}

</style>