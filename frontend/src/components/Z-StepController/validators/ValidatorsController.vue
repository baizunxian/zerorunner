<template>
  <div>
    <el-button type="primary" @click="add">
      添加断言
    </el-button>
  </div>

  <div class="extract-item-editing JsonPath" v-show="data">
    <div class="regex-item" v-for="(jsonPath, index) in data" :key="index">
      <el-row justify="space-between"
              align="middle"
              type="flex"
              style="margin: 0 -5px">
        <el-col :span="12">
          <div class="flex w100">
            <el-input type="primary"
                      link
                      style="width: 100%"
                      class="input-with-select"
                      maxlength="60"
                      :placeholder="getPlaceholder(jsonPath.mode)"
                      v-model="jsonPath.check">
              <template #prepend>
                <el-select size="small"
                           v-model="jsonPath.mode"
                           placeholder="提取方式"
                           @change="selectMode(jsonPath)"
                           filterable
                >
                  <el-option
                      v-for="item in state.modeTypes"
                      :key="item.key"
                      :label="item.key"
                      :value="item.value">
                  </el-option>
                </el-select>
              </template>
            </el-input>

            <div v-if="jsonPath.mode === 'JsonPath'"
                 class="flex pl10"
                 style="align-items: center;
                 width: 50%">
              <el-tag type="">继续提取</el-tag>
              <el-popover
                  placement="top"
                  trigger="hover"
                  content="提取结果是数组时可以开启此项，提取数组中的某一个值"
              >
                <template #reference>
                  <el-icon>
                    <ele-InfoFilled/>
                  </el-icon>
                </template>
              </el-popover>
              <el-switch v-model="jsonPath.continue_extract">
              </el-switch>
              <div>
                <el-input-number :disabled="!jsonPath.continue_extract"
                                 controls-position="right"
                                 style="padding-left: 5px"
                                 v-model="jsonPath.continue_index">
                </el-input-number>
              </div>

              <el-popover
                  placement="top"
                  :width="200"
                  trigger="hover"
                  content="0 表示第1项，1表示第2项，-1表示倒数第1项，-2表示倒数第2项，以此类推"
              >
                <template #reference>
                  <el-icon>
                    <ele-InfoFilled/>
                  </el-icon>
                </template>
              </el-popover>
            </div>
          </div>
        </el-col>

        <el-col :span="10">
          <el-input type=""
                    link
                    class="input-with-select"
                    placeholder="期望值"
                    clearable
                    v-model="jsonPath.expect">
            <template #prepend>
              <el-select size="small"
                         v-model="jsonPath.comparator"
                         placeholder="断言方式"
                         filterable>
                <el-option
                    v-for="(value, key) in state.comparators"
                    :key="key"
                    :label="value"
                    :value="key">
                </el-option>
              </el-select>
            </template>
          </el-input>

        </el-col>

        <el-col :span="1">
          <el-button type="danger" circle @click="deleted(index)">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </el-col>

      </el-row>
    </div>
  </div>

</template>

<script setup name="ValidatorsController">
import {reactive} from 'vue';
import {getComparators, getModeTypeObj, getPlaceholder} from "/@/utils/case";

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
})

const state = reactive({
  modeTypes: getModeTypeObj("validator"),
  comparators: getComparators("validator"),
  assertMode: "jmespath",
})

// add
const add = () => {
  props.data.push({
    mode: "jmespath",
    check: "",
    comparator: "equals",
    expect: "",
    continue_extract: false,
    continue_index: 0
  })
}

const deleted = (index) => {
  props.data.splice(index, 1)
}

const selectMode = (data) => {
  if (data.mode === 'JsonPath' && !data.continue_index) {
    data.continue_index = 0
  }
}

</script>

<style lang="scss" scoped>

.extract-item-editing {
  padding-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  //width: 100%;

  .regex-item {
    margin-top: 10px;
  }
}

.extract-item-editing.json {
  border-left: 2px solid #44b3d2;
}

.extract-item-editing.JsonPath {
  border-left: 2px solid #fca130;
}

:deep(.input-with-select .el-input-group__prepend) {
  background-color: var(--el-fill-color-blank);
}
</style>