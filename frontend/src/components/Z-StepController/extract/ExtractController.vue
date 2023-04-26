<template>
  <!--  <el-divider style="margin: 10px 0 5px 0;"/>-->
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
            v-for="value in state.extractTypes"
            :key="value"
            :label="value"
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
  <div class="extract-item-editing jmespath" v-show="isShowType('jmespath')">
    <div>jmespath</div>
    <div class="regex-item" v-for="(dataInfo, index) in data" :key="dataInfo">
      <el-row justify="space-between"
              v-if="dataInfo.extract_type === 'jmespath'"
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
  <div class="extract-item-editing JsonPath" v-show="isShowType('JsonPath')">
    <div>JsonPath</div>
    <div class="regex-item" v-for="(dataInfo, index) in data" :key="dataInfo">
      <el-row justify="space-between"
              align="middle"
              v-if="dataInfo.extract_type === 'JsonPath'"
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
        <el-col :span="8">
          <el-input type="primary"
                    link maxlength="60"
                    placeholder="jmespath表达式  列如：$.data.rows[0].id"
                    v-model="dataInfo.path">
          </el-input>
        </el-col>

        <el-col :span="6">
          <span>继续提取</span>
          <el-popover
              placement="top"
              :width="200"
              trigger="hover"
              content="提取结果是数组时可以开启此项，提取数组中的某一个值"
          >
            <template #reference>
              <el-icon>
                <ele-InfoFilled/>
              </el-icon>
            </template>
          </el-popover>
          <el-switch style="top: -2px;"
                     v-model="dataInfo.continue_extract"></el-switch>
          <el-input-number :disabled="!dataInfo.continue_extract"
                           controls-position="right"
                           style="padding-left: 5px"
                           v-model="dataInfo.continue_index">
          </el-input-number>
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
import {reactive, watch} from 'vue';
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
  extractTypes: ["jmespath", "JsonPath"],  // {"正则": 10, "JsonPath": 20}
  extract_type: "jmespath",
  extractTypeGroup: {},

})

// add JsonPathList
const add = () => {
  let addData: any
  if (state.extract_type == "jmespath") {
    addData = {name: "", path: "", extract_type: "jmespath"}
  } else if (state.extract_type == "JsonPath") {
    addData = {name: "", path: "", extract_type: "JsonPath", continue_extract: false, continue_index: 0}
  }
  if (props.data) {
    props.data?.push(addData)
  } else {
    emit("update:data", [addData])
  }
}

const deleted = (index: number) => {
  props.data.splice(index, 1)
}
const isShowType = (extractType: string) => {
  let isShow: boolean = false
  if (props.data && props.data.length > 0) {
    props.data.forEach((e: any) => {
      if (e.extract_type === extractType) {
        isShow = true
        return
      }
    })
  }
  return isShow
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

</style>