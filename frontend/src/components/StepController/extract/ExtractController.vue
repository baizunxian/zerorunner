<template>
  <el-divider style="margin: 10px 0 5px 0;"/>
  <div style="border: 1px solid #E6E6E6; padding: 8px">
    <div>

      <el-select size="small"
                 v-model="state.extract_type"
                 placeholder="提取方式"
                 filterable
                 clearable
                 style="width: 200px"
      >
        <el-option
            v-for="(value, key) in state.extractTypes"
            :key="key"
            :label="key"
            :value="value">
        </el-option>
      </el-select>

      <el-button type="primary"
                 style="margin-left: 5px"
                 :disabled="!state.extract_type"
                 @click="add">添加
      </el-button>
    </div>

  </div>
  <div class="extract-item-editing json" v-show="data?.length > 0">
    <div>jmespath</div>
    <div class="regex-item" v-for="(dataInfo, index) in data" :key="dataInfo">
      <el-row justify="space-between"
              align="middle"
              class="el-row--flex"
              style="margin: 0 -5px">
        <el-col :span="11" style="margin: 0 5px">
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
        <el-col :span="11">
          <el-input type="primary"
                    link maxlength="60"
                    placeholder="jmespath表达式  列如：body.data.0.id"
                    v-model="dataInfo.path">
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

<script lang="ts" setup name="ExtractController">
import {reactive} from 'vue';
import commonFunction from '/@/utils/commonFunction';

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
  // extractTypes
  extractTypes: ["jmespath"],  // {"正则": 10, "JsonPath": 20}
  extract_type: "jmespath",

})

// add JsonPathList
const add = () => {
  if (state.extract_type == "jmespath") {
    if (props.data) {
      props.data?.push({name: "", path: "", extract_type: "jmespath"})
    } else {
      emit("update:data", [{name: "", path: "", extract_type: "jmespath"}])
    }
  }
}

const deleted = (index: number) => {
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

.extract-item-editing.json {
  border-left: 2px solid #44b3d2;
}

</style>