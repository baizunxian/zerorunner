<template>
  <!-- data - table -->
  <div>
    <div class="block-title" style="display: flex; align-items: center;">
      <strong>
        <el-tooltip placement="bottom-start">
          提取
          <!--          <el-icon><ele-InfoFilled /></el-icon>-->
          <template #content>
            从当前 HTTP
            请求的响应结果中提取参数，并保存到参数变量中（例如token），后续测试用例可通过${token}的形式进行引用<br/>
            <br/>参数名：可以自定义名称<br/>
            参数值：响应结果中的参数值<br/>
            <br/>样例：content 相当于返回的body内容, 返回内容为 {code: 0, msg: 'OK'}，要提取msg的格式为body.msg<br/>
          </template>

        </el-tooltip>
      </strong>

      <el-button size="small" type="primary" link @click="addExtract" title="新增提取">
        <el-icon>
          <ele-CirclePlusFilled></ele-CirclePlusFilled>
        </el-icon>
        add
      </el-button>

    </div>
    <el-table
        ref="extractTableRef"
        :data="state.extract"
        border
        tooltip-effect="dark"
        style="width: 100%"
    >
      <!-- <el-table-column type="selection" width="55" label="Option">
      </el-table-column> -->
      <el-table-column header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">变量名</strong>
        </template>
        <template #default="scope">
          <el-input size="small" v-model="scope.row.key"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="value" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">提取值</strong>
        </template>
        <template #default="scope">
          <el-input size="small" v-model="scope.row.value"></el-input>
        </template>
      </el-table-column>
      <el-table-column align="center" width="50" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="deleteExtract(scope.$index)">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- headers -->
    <div class="block-title" style="display: flex; align-items: center;">

      <el-tooltip placement="bottom-start">
        <strong>校验</strong>
        <template #content>
          测试用例中定义的结果校验项，作用域为当前测试用例，用于实现对当前测试用例运行结果的校验<br/>
          <br/>校验参数：响应结果中的参数<br/>
          对比规则：校验参数与校验值对比的规则<br/>
          类型：校验值的数据类型<br/>
          校验值：跟校验参数进行对比的值<br/>
          <br/>样例：返回内容为 {code: 0, msg: 'OK'}，要校验msg等于OK， 校验参数格式为body.msg，对比规则为equals，类型为String，校验值为OK<br/>
        </template>
        <!--        <el-icon><ele-info-filled /></el-icon>-->

        <i class="el-icon-info" style="color:#409eff;margin-left:5px;"></i>
      </el-tooltip>

      <el-button size="small" type="primary" link @click="addValidate" title="新增校验">
        <el-icon>
          <ele-CirclePlusFilled></ele-CirclePlusFilled>
        </el-icon>
        add
      </el-button>
      <!--      <el-button class="filter-item" type="success" icon="el-icon-plus" round size="mini" style="padding: 4px;"-->
      <!--                 title="新增校验" @click="addValidate"></el-button>-->
    </div>
    <el-table
        ref="validateTableRef"
        :data="state.validate"
        border
        tooltip-effect="dark"
        style="width: 100%"
    >
      <el-table-column prop="key" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">校验参数</strong>
        </template>
        <template #default="scope">
          <el-input size="small" v-model="scope.row.check"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="Comparator" width="120" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">对比规则</strong>
        </template>
        <template #default="scope">
          <el-select size="small" v-model="scope.row.comparator" placeholder="请选择">
            <el-option
                v-for="item in state.comparatorOptions"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
          </el-select>
        </template>
      </el-table-column>

      <el-table-column prop="type" width="120" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">类型</strong>
        </template>
        <template #default="scope">
          <el-select size="small" v-model="scope.row.type" placeholder="请选择">
            <el-option
                v-for="item in state.typeOptions"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
          </el-select>
        </template>
      </el-table-column>

      <el-table-column prop="Expected" label="Expected" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">校验值</strong>
        </template>
        <template #default="scope">
          <el-input size="small" v-model="scope.row.expected"></el-input>
        </template>
      </el-table-column>
      <el-table-column align="center" width="50" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="deleteValidate(scope.$index)">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup name="ExtractValidate">

import {reactive, ref} from "vue";

const formRef = ref()
const state = reactive({
  extract: [],   // 提取参数
  validate: [],  // 校验参数
  typeOptions: ['string', 'int', 'float', 'boolean', 'dict', 'list'],  // 数据类型
  comparatorOptions: [  // 校验方法
    'equals',
    'contains',
    'startswith',
    'endswith',
    'regex_match',
    'type_match',
    'contained_by',
    'less_than',
    'less_than_or_equals',
    'greater_than',
    'greater_than_or_equals',
    'not_equal',
    'string_equals',
    'length_equals',
    'length_greater_than',
    'length_greater_than_or_equals',
    'length_less_than',
    'length_less_than_or_equals',
    'json_equals',
  ],

});
// 初始化数据
const initForm = (formData) => {
  state.extract = []
  state.validate = []
  if (formData && formData.extract && formData.extract.length > 0) {
    formData.extract.forEach((extracts) => {
      for (let key in extracts) {
        let extract_dict = {
          key: key,
          value: extracts[key]
        }
        state.extract.push(extract_dict)
      }
    })
  }
  if (formData && formData.validate && formData.validate.length > 0) {
    formData.validate.forEach(valid => {
      // 后台数据是按类型返回的，前端数据存储转为string
      if (typeof (valid.expected) === 'object') {
        valid['expected'] = JSON.stringify(valid.expected)
      } else {
        valid['expected'] = valid.expected.toString()
      }
      state.validate.push(valid)
    })
  }
}

// 获取表单数据
const getFormData = () => {
  let from = {
    extract: [],
    validate: [],
  }
  if (state.extract.length > 0) {
    state.extract.forEach(ext => {
      if (ext.key !== '') {
        let extracts = {}
        extracts[ext.key] = ext.value
        from.extract.push(extracts)
      }
    })
  }
  if (state.validate && state.validate.length > 0) {
    from.validate = state.validate
  }
  return from
}

// extract
const addExtract = () => {
  state.extract.push({key: '', value: 'body.'})
}
const deleteExtract = (index) => {
  state.extract.splice(index, 1)
}

// validate
const addValidate = () => {
  state.validate.push({check: 'body.', comparator: 'equals', type: 'string', expected: ''})
}
const deleteValidate = (index) => {
  state.validate.splice(index, 1)
}

defineExpose({
  formRef,
  initForm,
  getFormData,
  addExtract,
  deleteExtract,
  addValidate,
  deleteValidate,
})

</script>

<style lang="scss" scoped>
.filter-item {
  color: #fff;
  background-color: #5bc0de;
  border-color: #ffffff;

  &:hover {
    color: #fff;
    background-color: #31b0d5;
    border-color: #ffffff;
  }
}

/* el-input */
:deep(.el-input__inner) {
  font-weight: bold;
}

.block-title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 28px;
  line-height: 28px;
  background: #f7f7fc;
  color: #333333;
}
</style>