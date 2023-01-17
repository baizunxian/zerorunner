<template>
  <!-- data - table -->
  <div>
    <div class="block-title" style="display: flex; align-items: center;">
      <el-tooltip placement="bottom-start">
        <strong>变量</strong>
        <template #content>
          定义的全局变量，作用域为整个用例
          <br/>
          <br/>参数名：可以自定义名称<br/>
          类型：参数值的数据类型<br/>
          参数值：变量对应的值<br/>
          备注：变量信息描述<br/>
          <br/>
          加密：想要变量值加密需要变量名加上__encryption后缀 <br/>
          例如有个变量名是 pwd 想对 pwd 对应的值加密 则变量名改完 pwd__encryption 保存后对应的值加密<br/>
          <br/>样例：定义一个名称为id，值为10000的变量，格式为参数名id，类型为int，参数值为10000<br/>
        </template>
      </el-tooltip>

      <el-button type="primary" link @click="addVariables" title="新增变量">
        <el-icon>
          <ele-CirclePlusFilled></ele-CirclePlusFilled>
        </el-icon>
        add
      </el-button>

    </div>
    <el-table
        ref="multipleTable"
        :data="variables"
        border
        tooltip-effect="dark"
        style="width: 100%"
    >
      <el-table-column type="selection" width="55" label="Option">
      </el-table-column>
      <el-table-column header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">变量名</strong>
        </template>
        <template #default="scope">
          <el-input v-model="scope.row.key"></el-input>
        </template>
      </el-table-column>

      <el-table-column prop="type" width="120" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">类型</strong>
        </template>
        <template #default="scope">
          <el-select v-model="scope.row.type" placeholder="请选择">
            <el-option
                v-for="item in typeOptions"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
          </el-select>
        </template>
      </el-table-column>

      <el-table-column prop="value" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">变量值</strong>
        </template>
        <template #default="scope">
          <el-input v-model="scope.row.value"></el-input>
        </template>
      </el-table-column>

      <el-table-column prop="remarks_" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">备注</strong>
        </template>
        <template #default="scope">
          <el-input v-model="scope.row.remarks_"></el-input>
        </template>
      </el-table-column>

      <el-table-column align="center" width="50" class-name="small-padding fixed-width">
        <template #default="scope">

          <el-button size="small" type="primary" link @click="deleteVariables(scope.$index)">
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
        <strong>参数</strong>
        <template #content>
          全局参数，用于实现数据化驱动，作用域为整个用例<br/>
          <br/>参数名：可以自定义名称<br/>
          参数值：参数对应的值<br/>
          备注：参数信息描述<br/>
          <br/>样例1：定义单个参数，参数有两个值格式，参数名称为name1，参数值["value1","value2"]<br/>
          <br/>样例2：定义多个参数，每个参数有两个值格式，参数名称为name1，name2，参数值[["name1_value1","name1_value2"],["name2_value1","name2_value2"]]<br/>
        </template>
      </el-tooltip>

      <el-button type="primary" link @click="addParameters" title="新增参数">
        <el-icon>
          <ele-CirclePlusFilled></ele-CirclePlusFilled>
        </el-icon>
        add
      </el-button>

      <!--
            <el-button class="filter-item" type="success" icon="el-icon-plus"  round size="mini" style="padding: 4px;" title="新增参数" @click="csvUpload">导入</el-button>
      -->
    </div>
    <el-table
        ref="parametersTableRef"
        :data="parameters"
        border
        tooltip-effect="dark"
        style="width: 100%"
    >

      <el-table-column prop="Key" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">参数名</strong>
        </template>
        <template #default="scope">
          <el-input type="textarea" v-model="scope.row.key" :placeholder="ValueV"></el-input>
        </template>
      </el-table-column>

      <el-table-column label="Value" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">参数值</strong>
        </template>
        <template #default="scope">
          <el-input type="textarea" v-model="scope.row.value" :placeholder="ValueP"></el-input>
        </template>
      </el-table-column>

      <el-table-column label="remarks_" header-align='center' width="250">
        <template #header>
          <strong style="font-size: 14px;">备注</strong>
        </template>
        <template #default="scope">
          <el-input type="textarea" v-model="scope.row.remarks_"></el-input>
        </template>
      </el-table-column>

      <el-table-column align="center" width="150" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="deleteParameters(scope.$index)">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

<!--    <div class="block-title" style="display: flex; align-items: center;">-->

<!--      <el-tooltip placement="bottom-start">-->
<!--        <strong>函数</strong>-->
<!--        <template #content>-->
<!--          前置函数：在 HTTP 请求发送前执行 hook 函数，主要用于准备工作<br/>-->
<!--          后置函数：在 HTTP 请求发送后执行 hook 函数，主要用户测试后的清理工作<br/>-->
<!--        </template>-->
<!--      </el-tooltip>-->

<!--      <el-button type="primary" link @click="addHooks" title="新增函数">-->
<!--        <el-icon>-->
<!--          <ele-CirclePlusFilled></ele-CirclePlusFilled>-->
<!--        </el-icon>-->
<!--        add-->
<!--      </el-button>-->

<!--    </div>-->
<!--    <el-table-->
<!--        ref="hooksTableRef"-->
<!--        :data="hooks"-->
<!--        border-->
<!--        tooltip-effect="dark"-->
<!--        style="width: 100%"-->
<!--    >-->
<!--      <el-table-column label="key" header-align='center'>-->
<!--        <template #header>-->
<!--          <strong style="font-size: 14px;">前置函数</strong>-->
<!--        </template>-->
<!--        <template #default="scope">-->
<!--          <el-input v-model="scope.row.setup_hooks"></el-input>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column prop="value" header-align='center'>-->
<!--        <template #header>-->
<!--          <strong style="font-size: 14px;">后置函数</strong>-->
<!--        </template>-->
<!--        <template #default="scope">-->
<!--          <el-input v-model="scope.row.teardown_hooks"></el-input>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column align="center" width="50" class-name="small-padding fixed-width">-->
<!--        <template #default="scope">-->
<!--          <el-button size="small" type="primary" link @click="deleteHooks(scope.$index)">-->
<!--            <el-icon>-->
<!--              <ele-Delete/>-->
<!--            </el-icon>-->
<!--          </el-button>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--    </el-table>-->
  </div>
</template>

<script lang="ts">

interface baseState {
  key: string,
  value: string,
  remarks_: string
}

interface variablesState extends baseState {
  type: string
}

interface hooksState {
  setup_hooks: string,
  teardown_hooks: string
}

interface formDataState {
  variables: Array<variablesState>,
  parameters: Array<baseState>,
  setup_hooks: Array<hooksState>,
  teardown_hooks: Array<hooksState>,
}

interface state {
  variables: Array<variablesState>,
  parameters: Array<baseState>,
  hooks: Array<hooksState>,
  ValueV: string,
  ValueP: string,
  typeOptions: Array<string>,
}

import {defineComponent, reactive, ref, toRefs} from "vue";

export default defineComponent({
  name: 'variablesParameters',
  components: {},
  setup() {
    const formRef = ref()
    const state = reactive<state>({
      variables: [],   // 变量列表
      parameters: [{key: '', value: '', remarks_: ''}],  //  参数列表
      hooks: [],  // 钩子函数列表
      ValueV: '多参数示例：a,b    单参数示例： c',
      ValueP: '多参数示例: [["name1", "pwd1"],["name2","pwd2"]]   单参数示例: [1, "value2"]',
      typeOptions: ['string', 'int', 'float', 'boolean'],

    });
    // 初始化数据
    const initForm = (formData: formDataState) => {
      state.variables = []
      state.parameters = []
      state.hooks = []
      state.parameters = [{key: '', value: '', remarks_: ''}]

      if (formData && formData.variables && formData.variables.length > 0) {
        state.variables = formData.variables
      }
      if (formData.parameters) {
        state.parameters = []
        formData.parameters.forEach(p => {
          if (typeof p['value'] == 'string') {
            state.parameters.push({key: p['key'], value: p['value'], remarks_: p['remarks_']})
          } else {
            state.parameters.push({key: p['key'], value: JSON.stringify(p['value']), remarks_: p['remarks_']})
          }
        })
      }
      if (formData && formData.setup_hooks && formData.teardown_hooks) {
        let setup_hooks = formData.setup_hooks
        let teardown_hooks = formData.teardown_hooks
        setup_hooks.forEach((hook: string, index: number) => {
          let hookData: hooksState = {setup_hooks: hook, teardown_hooks: teardown_hooks[index]}
          state.hooks.push(hookData)
        })
        // this.hooks = form.hooks
      }

    }

    // 获取表单数据
    const getFormData = () => {
      let form = {
        variables: [],
        parameters: [],
        setup_hooks: [],
        teardown_hooks: [],
      }
      console.log(state, 'vpvariables STate')
      if (state.variables.length > 0) {
        state.variables.forEach(data => {
          if (data.key !== '' && data.type === 'string') {
            data.value = data.value.replace(/'/g, '"')
            form.variables.push(data)
          } else {
            form.variables.push(data)
          }
          console.log(form, 'from==============')
        })
      }
      if (state.parameters.length > 0) {
        state.parameters.forEach(data => {
          if (data.key !== '') {
            data.value = data.value.replace(/'/g, '"')
            form.parameters.push(data)
          }
        })
      }
      if (state.hooks.length > 0) {
        state.hooks.forEach(data => {
          if (data.key !== '') {
            form.setup_hooks.push(data.setup_hooks)
            form.teardown_hooks.push(data.teardown_hooks)
          }
        })
      }
      console.log(form)
      return form
    }

    // variables
    const addVariables = () => {
      state.variables.push({key: '', type: 'string', value: '', remarks_: ''})
    }
    const deleteVariables = (index: number) => {
      state.variables.splice(index, 1)
    }

    // parameters
    const addParameters = () => {
      state.parameters.push({key: '', value: '', remarks_: ''})
    }
    const deleteParameters = (index: number) => {
      state.parameters.splice(index, 1)
    }

    // hooks
    const addHooks = () => {
      state.hooks.push({setup_hooks: '', teardown_hooks: ''})
    }
    const deleteHooks = (index: number) => {
      state.hooks.splice(index, 1)
    }

    return {
      formRef,
      initForm,
      getFormData,
      addVariables,
      deleteVariables,
      addParameters,
      deleteParameters,
      addHooks,
      deleteHooks,
      ...toRefs(state),
    };
  },
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
:deep(.el-textarea__inner) {
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