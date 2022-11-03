<template>
  <div>
    <el-select size="small"
               v-model="assertMode"
               placeholder="提取方式"
               filterable
               clearable
               style="width: 200px">
      <el-option
          v-for="(value, index) in assertModes"
          :key="index"
          :label="value"
          :value="value">
      </el-option>
    </el-select>

    <el-button type="primary"
               style="margin-left: 5px"
               :disabled="!assertMode"
               @click="add">添加
    </el-button>
  </div>

  <div class="extract-item-editing json" v-show="data?.length>0">
    <div>JsonPath</div>
    <div class="regex-item" v-for="(jsonPath, index) in data" :key="index">
      <el-row justify="space-between" align="middle" class="el-row--flex"
              style="margin: 0 -5px">
        <el-col :span="12">
          <el-input type="primary" link maxlength="60" placeholder="JsonPath表达式" v-model="jsonPath.check">
          </el-input>
        </el-col>

        <el-col :span="5">
          <el-select size="small"
                     v-model="jsonPath.comparator"
                     placeholder="提取方式"
                     filterable
                     clearable
                     style="width: 100%"
          >
            <el-option
                v-for="(value, key) in comparators[jsonPath.mode]"
                :key="key"
                :label="value"
                :value="key">
            </el-option>
          </el-select>
        </el-col>

        <el-col :span="5" style="margin: 0 5px">
          <el-input type="primary" link placeholder="期望值" v-model="jsonPath.expect">
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

<script lang="ts">
import {defineComponent, reactive, toRefs} from 'vue';

export default defineComponent({
  name: 'validatorsController',  //断言规则
  props: {
    data: Object,
    default: () => []
  },
  emits: ['update:data'],
  setup(props) {
    const state = reactive({
      assertModes: ["JsonPath"],  // {"正则": 10, "JsonPath": 20}
      comparators: {
        jsonPath: {
          equals: "等于",
          not_equals: "不等",
          length_equals: "长度等于",
          contains: "包含",
          startswith: "以...开始",
          endswith: "以...结束",
          regex_match: "正则",
          type_match: "类型等于",
          less_than: "小于",
          less_than_or_equals: "小于或者等于",
          greater_than: "大于或等于",
          greater_than_or_equals: "大于或等于",
        }
      },
      assertMode: "JsonPath",
      //JsonPathList
      // JsonPathList: [{name: "test", path: "$.*"}],
      // data: {
      //   mode: "jsonPath",  // 断言模式
      //   check: "jsonPath",  // 校验值
      //   comparator: "jsonPath", // 校验方式
      //   expected: "jsonPath",   // 预期值
      // }

    })

    // add JsonPathList
    const add = () => {
      if (state.assertMode == "JsonPath") {
        props.data.push({mode: "jsonPath", check: "", comparator: "", expect: ""})
      } else if (state.assertType == 20) {
        props.data.push({name: "", json_path: ""})
      }
    }

    const deleted = (index: number) => {
      props.data.splice(index, 1)
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