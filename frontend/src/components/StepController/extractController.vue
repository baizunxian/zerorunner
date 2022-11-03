<template>
  <el-collapse-transition>
    <div v-show="data.showDetail" @click.stop="">
      <el-divider style="margin: 10px 0 5px 0;"/>
      <div style="border: 1px solid #E6E6E6; padding: 8px">
        <div>

          <el-select size="small"
                     v-model="extractType"
                     placeholder="提取方式"
                     filterable
                     clearable
                     style="width: 200px"
          >
            <el-option
                v-for="(value, key) in extractTypes"
                :key="key"
                :label="key"
                :value="value">
            </el-option>
          </el-select>

          <el-button type="primary"
                     style="margin-left: 5px"
                     :disabled="!extractType"
                     @click="add">添加
          </el-button>
        </div>

      </div>

      <div class="extract-item-editing json" v-show="data.value?.length>0">
        <div>JsonPath</div>
        <div class="regex-item" v-for="(jsonPath, index) in data.value" :key="jsonPath">
          <el-row justify="space-between" align="middle" class="el-row--flex"
                  style="margin: 0 -5px">
            <el-col :span="11" style="margin: 0 5px">
              <el-input type="primary" link maxlength="60" placeholder="变量名" v-model="jsonPath.name">
                <template #suffix>
                  {{ jsonPath.name.length }}/60
                </template>
              </el-input>
            </el-col>
            <el-col :span="11">
              <el-input type="primary" link maxlength="60" placeholder="JsonPath表达式" v-model="jsonPath.path">
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
    </div>
  </el-collapse-transition>

</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'extractController',
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup(props) {
    const state = reactive({
      // extractTypes
      extractTypes: ["JsonPath"],  // {"正则": 10, "JsonPath": 20}
      extractType: "JsonPath",

    })

    // add JsonPathList
    const add = () => {
      if (state.extractType == "JsonPath") {
        if (props.data.value) {
          props.data.value?.push({name: "", json_path: "", extractType: "JsonPath"})
        } else {
          props.data.value = [{name: "", json_path: "", extractType: "JsonPath"}]
        }
      }
    }

    const deleted = (index: number) => {
      props.data.value.splice(index, 1)
    }

    return {
      add,
      deleted,
      ...toRefs(state),
    };
  },
});
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