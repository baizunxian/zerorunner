<template>
  <div style="padding: 8px">
    <div>
      <el-button type="primary" @click="add">
        添加提取
      </el-button>
    </div>

    <div class="extract-item-editing jmespath" v-show="data">
      <div class="regex-item" v-for="(dataInfo, index) in data" :key="dataInfo">
        <el-row justify="space-between"
                align="middle"
                class="el-row--flex"
                style="margin: 0 -5px">
          <el-col :span="8" style="margin: 0 5px">
            <el-input type="primary" link maxlength="60" placeholder="变量名" v-model="dataInfo.name">
              <template #suffix>
                    <span class="el-input__suffix-inner" @click="copyText('${'+ dataInfo.name +'}')">
                      {{ dataInfo.name?.length }}/60
                      <el-icon color="#303133">
                        <ele-DocumentCopy/>
                      </el-icon>
                    </span>
              </template>
            </el-input>
          </el-col>

          <el-col :span="14" >
            <div class="flex w100">
              <el-input type="primary"
                        link
                        style="width: 100%"
                        class="input-with-select"
                        maxlength="60"
                        :placeholder="getPlaceholder(dataInfo.extract_type)"
                        v-model="dataInfo.path">
                <template #prepend>
                  <el-select size="small"
                             v-model="dataInfo.extract_type"
                             placeholder="提取方式"
                             filterable>
                    <el-option
                        v-for="item in state.modeTypes"
                        :key="item.key"
                        :label="item.key"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </template>

              </el-input>

              <div v-if="dataInfo.extract_type === 'JsonPath'"
                   class="flex pl10"
                   style="align-items: center; width: 40%">
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
                <el-switch v-model="dataInfo.continue_extract">
                </el-switch>
                <div>
                  <el-input-number :disabled="!dataInfo.continue_extract"
                                   controls-position="right"
                                   style="padding-left: 5px"
                                   v-model="dataInfo.continue_index">
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
  </div>
</template>

<script setup name="ExtractController">
import {reactive} from 'vue';
import commonFunction from '/@/utils/commonFunction';
import {getModeTypeObj, getPlaceholder} from "/@/utils/case";

const emit = defineEmits(['update:data'])

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})


const {copyText} = commonFunction()
const state = reactive({
  // modeTypes
  modeTypes: getModeTypeObj("extract"),
  extract_type: "jmespath",
  extractTypeGroup: {},

})

// add JsonPathList
const add = () => {
  let data
  data = {name: "", path: "", extract_type: "jmespath"}
  if (props.data) {
    props.data?.push(data)
  } else {
    emit("update:data", [data])
  }
}

const deleted = (index) => {
  props.data.splice(index, 1)
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

.extract-item-editing.jmespath {
  border-left: 2px solid #44b3d2;
}

.extract-item-editing.JsonPath {
  border-left: 2px solid #fca130;
}

:deep(.input-with-select .el-input-group__prepend) {
  background-color: var(--el-fill-color-blank);
}

</style>