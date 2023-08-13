<template>
  <el-table
      v-if="state.showStepTable"
      class="ui-case-step"
      :data="stepData"
      rowKey="index"
      ref="tableRef">

    <el-table-column width="40" align="center">
      <template #default="{row}">
        <span class="move">
        <el-icon class="step-rank"><Rank></Rank></el-icon>
          </span>
      </template>
    </el-table-column>

    <el-table-column type="expand" width="30">
      <template #default="{row}">
        <div style="padding: 0 30px">
          <z-monaco-editor style="height: 200px"
                           long="python"
                           v-model:value="row.script">
          </z-monaco-editor>
        </div>
      </template>
    </el-table-column>

    <el-table-column prop="index" label="序号" width="40" align="center">
      <template #default="{row}">
        <span>{{ row.index }}</span>
      </template>
    </el-table-column>

    <el-table-column prop="name" label="启用" width="40" align="center">
      <template #default="{row}">
        <el-checkbox v-model="row.enable"></el-checkbox>
      </template>
    </el-table-column>

    <el-table-column v-if="useType === 'debug'" prop="name" label="断点" width="40" align="center">
      <template #default="{row}">
        <div :class="[row.breakpoint === true? 'step-breakpoint-danger': 'step-breakpoint-info']"
             class="el-step__icon is-text"
             @click="handelBreakpoint(row)"></div>
      </template>
    </el-table-column>

    <el-table-column prop="name" label="步骤名称">
      <template #default="{row}">
        <el-input v-model.lazy="row.name"></el-input>
      </template>
    </el-table-column>

    <el-table-column prop="name" label="name">
      <template #header>
        <div>
          <span style="margin-right: 10px">页面元素</span>
          <el-button type="success"
                     v-show="!useType"
                     @click="getAllPageElement"
                     round
                     :icon="RefreshLeft">刷新
          </el-button>
        </div>
      </template>
      <template #default="{row}">
        <el-cascader v-model.lazy="row.page_element_id"
                     style="width: 100%"
                     @change="(value: any) => pageElementChange(value, row)"
                     placeholder="请选择页面元素"
                     :clearable="true"
                     :props="{expandTrigger: 'hover',
                              value: 'id',
                              label: 'name',
                              children: 'elements'}"
                     :options="state.pageElementList"></el-cascader>
      </template>
    </el-table-column>

    <el-table-column>
      <template #header>
        <div>
          <span style="margin-right: 10px">动作</span>
          <el-button type="success"
                     v-show="!useType"
                     @click="getAllPageElement"
                     round
                     :icon="RefreshLeft">刷新
          </el-button>
        </div>
      </template>
      <template #default="{row}">
        <el-cascader v-model.lazy="row.action_value"
                     style="width: 100%"
                     @change="(value: any) => {
                         row.action = value ? value[1] : ''
                       }"
                     placeholder="请选择动作"
                     :clearable="true"
                     :props="{expandTrigger: 'hover',
                                children: 'actions',}"
                     :options="state.actions"></el-cascader>
      </template>
    </el-table-column>

    <el-table-column prop="data" label="操作数据/结果">
      <template #default="scope">
        <el-input v-model.lazy="scope.row.data" placeholder="请输入数据"></el-input>
      </template>
    </el-table-column>

    <el-table-column prop="data" label="" width="250">
      <template #header>
        <div v-if="!useType">
          <el-button type="primary" @click="handelAddUiCase" round :icon="CirclePlus">引用用例</el-button>
          <el-button type="success" @click="addStep" round :icon="CirclePlus">测试步骤</el-button>
        </div>
        <div v-else>
          <el-button type="success" @click="addStep" round :icon="CirclePlus">点击添加步骤</el-button>
        </div>
      </template>
      <template #default="scope">
        <el-button type="primary" @click="moveStep(scope.$index, 'up')">
          <el-icon>
            <Top></Top>
          </el-icon>
        </el-button>
        <el-button type="primary" @click="moveStep(scope.$index,'down')">
          <el-icon>
            <Bottom></Bottom>
          </el-icon>
        </el-button>
        <el-button v-show="!useType" type="warning" @click="copyCaseStep(scope.row)">复制</el-button>
        <el-button v-show="!useType" type="danger" @click="deletedCaseStep(scope.$index)">删除</el-button>
        <el-button v-show="useType" type="danger" @click="copyCaseStep">调试</el-button>
      </template>
    </el-table-column>

  </el-table>

</template>

<script setup lang="ts" name="EditPage">
import {ElButton, ElCascader, ElInput, ElCheckbox} from "element-plus";
import {computed, h, nextTick, onMounted, reactive, ref, watch} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import {CirclePlus, RefreshLeft, Top, Bottom, Rank} from "@element-plus/icons-vue"
import MonacoEditor from "/@/components/monaco/index.vue";
import Sortable from "sortablejs";

const tableRef = ref()

const props = defineProps({
  stepDataList: {
    type: Array,
    default: () => {
      return []
    }
  },
  useType: {
    type: String,
    default: ''
  },
})

const emit = defineEmits(["update:stepDataList", "update:data"])

const state = reactive({
  columns: [
    {
      key: 'rank', label: 'rank', prop: '', width: '60', align: 'center', show: true,
      render: ({row}: any) => h(Rank, {}),
    },
    {
      key: 'script', prop: 'script', label: '', columnType: 'expand', width: '30', show: true,
      render: ({row}: any) => h(MonacoEditor, {
        value: row.script,
        language: 'python',
        style: {
          height: '200px',
          width: '100%',
          margin: '0 30px',
        },
        "onUpdate:value": (val: any) => {
          console.log(val, 'val')
          row.script = val
        },
        options: {
          readOnly: false,
          minimap: {
            enabled: false
          }
        }
      })
    },
    {label: '序号', columnType: 'index', width: '50', show: true},
    {
      key: 'enable', label: '启用', prop: 'enable', width: '60', align: 'center', show: true,
      render: ({row}: any) => h(ElCheckbox, {
        modelValue: row.enable,
      }),
    },
    {
      key: 'name', label: '步骤名称', prop: 'name', align: 'center', show: true,
      render: ({row}: any) => h(ElInput, {
        modelValue: row.name,
        placeholder: '请输入描述',
        clearable: true,
      }),
    },
    {
      key: 'page_element_id',
      label: '页面元素',
      prop: 'page_element_id',
      align: 'center',
      show: true,
      render: ({row}: any) => h(ElCascader, {
        modelValue: row.page_element_id,
        options: state.pageElementList,
        style: {width: '100%'},
        onChange: (value: any) => {
          row.page_id = value ? value[0] : ''
          row.element_id = value ? value[1] : ''
        },
        props: {
          expandTrigger: 'hover',
          value: 'id',
          label: 'name',
          children: 'element',
        },
        placeholder: '请选择页面元素',
        clearable: true,
      }),
      renderHeader: () => h('div', {}, [
        h('span', {
          style: 'margin-right: 10px'
        }, "页面元素"),
        h(ElButton, {
          type: "success",
          icon: RefreshLeft,
          round: true,
          onClick: () => {
            getAllPageElement()
          }
        }, () => "刷新")
      ])

    },
    {
      key: 'action_value',
      label: '动作',
      prop: 'action_value',
      align: 'center',
      show: true,
      render: ({row}: any) => h(ElCascader, {
        modelValue: row.action_value,
        options: state.actions,
        onChange: (value: any) => {
          row.action = value ? value[1] : ''
        },
        style: {width: '100%'},
        props: {
          expandTrigger: 'hover',
          children: 'actions',
        },
        placeholder: '请选择动作',
        clearable: true,
      }),
    },
    {
      key: 'data',
      label: '操作数据/结果',
      prop: 'data',
      align: 'center',
      show: true,
      render: ({row}: any) => h(ElInput, {
        modelValue: row.data,
        placeholder: '请输入数据',
        clearable: true,
      }),
    },
    {
      label: '操作', fixed: 'right', width: '', align: 'center',
      render: ({row, $index}: any) => h("div", null, [
        h(ElButton, {
          type: "warning",
          onClick: () => {
            copyCaseStep(row)
          }
        }, () => "复制"),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deletedCaseStep($index)
          }
        }, () => '删除')
      ]),
      renderHeader: () => h('div', {}, [
        h(ElButton, {
          type: "success",
          icon: CirclePlus,
          round: true,
          onClick: () => {
            addStep()
          }
        }, () => "测试步骤")
      ])
    },
  ],
  actions: [
    {
      label: "常规操作", value: "常规操作", actions: [
        {label: "open(打开页面)", value: "open",},
        {label: "input(输入值)", value: "input",},
        {label: "click(点击)", value: "click",},
      ]
    },
  ],
  stepDataList: [],
  // pageElementList
  pageElementList: [],
//
  showStepTable: true,
});

const stepData = computed({
  get() {
    return props.stepDataList
  },
  set(val) {
    console.log(val, 'val111111111')
    emit('update:stepDataList', val)
  }
})

const getAllPageElement = () => {
  useUiPageApi().getAllPageElement({})
      .then(res => {
        state.pageElementList = res.data
      })
}

const handelAddUiCase = () => {

}

const addStep = () => {
  let step = {
    name: "",
    action: "",
    action_value: "",
    enable: true,
    data: "",
    page_element_id: "",
    page_id: null,
    element_id: null,
    location_method: "",
    location_value: "",
    cookie: "",
    script: "",
    output: ""
  }
  stepData.value.push(step)
}


const copyCaseStep = (row: any) => {
  console.log(row, 'row')
  let newRow = JSON.parse(JSON.stringify(row))
  stepData.value.push(newRow)
  // state.stepDataList.push(stepData)
}

const deletedCaseStep = (index: number) => {
  // state.stepDataList.splice(index, 1)
  stepData.value.splice(index, 1)
}

const handelBreakpoint = (row: any) => {
  row.breakpoint = !row.breakpoint
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data: any) => {
  if (data) {
    data.forEach((data: any, index: number) => {
      data.index = index + 1
    })
  }
}

// pageElementChange
const pageElementChange = (value: any, row: any) => {
  row.page_id = row.page_element_id ? row.page_element_id[0] : ''
  row.element_id = row.page_element_id ? row.page_element_id[1] : ''
  let pageInfo = state.pageElementList.find((item: any) => item.id === row.page_id)
  console.log(pageInfo, 'pageInfo')
  if (pageInfo && pageInfo.elements) {
    let elementInfo = pageInfo.elements.find((item: any) => item.id === row.element_id)
    if (elementInfo) {
      row.location_method = elementInfo.location_method
      row.location_value = elementInfo.location_value
    }
  }
}

// 移动数据
const moveStep = (index: number, type: string) => {
  let deleteData = stepData.value.splice(index, 1)   //截取数组里的一个数据
  let start = null
  if (type === 'up') {
    start = index === 0 ? 0 : index - 1
  } else {
    start = index === stepData.value.length ? index : index + 1
  }
  stepData.value.splice(start, 0, ...deleteData)   //在数组里插入一条数据
}

const createSortable = () => {
  // let tableList = tableRef.value.$el.querySelector('.ui-case-step .el-table__body-wrapper tbody')
  // console.log(tableList, 'tableList')
  // let el
  // if (tableList && tableList.length > 0) {
  //   el = tableList[0].querySelector('tbody')
  // }
  // console.log(11111111111)
  // console.log(el, 'el')
  // if (el) {
  Sortable.create(tableRef.value.$el.querySelector('.ui-case-step .el-table__body-wrapper tbody')), {
    animation: 150,
    sort: true,
    handle: ".move",
    // draggable: '.icon-step-rank', // 设置可拖拽行的类名(el-table自带的类名)
    forceFallback: true,
    onStart: () => {
      console.log("开始拖动");
    },
    onEnd: onEndFunc
    // }
  }
}

const onEndFunc = ({newIndex, oldIndex}: any) => {

  console.log(stepData.value, 'stepDataList')
  console.log(newIndex, 'newIndex')
  stepData.value.splice(newIndex, 0, stepData.value.splice(oldIndex, 1)[0])
  // state.showStepTable = false
  // nextTick(() => {
  //   state.showStepTable = true
  //   nextTick(() => {
  //     createSortable()
  //   })
  // })
}


onMounted(() => {
  getAllPageElement()
  nextTick(() => {
    createSortable()
  })
})

watch(
    () => props.data,
    (val) => {
      let newData = JSON.parse(JSON.stringify(val))
      newData.project_module = [newData.project_id, newData.module_id]
      state.form = newData
    },
    {
      deep: true,
    }
);

watch(
    () => stepData.value,
    (val) => {
      console.log(val, 'stepDataList111')
      computeDataIndex(stepData.value)
    },
    {
      deep: true,
    }
);

</script>

<style scoped lang="scss">
:deep(.el-table .el-table__cell) {
  padding: 8px 0;

}

.step-breakpoint-info {
  background: var(--el-color-info);
}

.step-breakpoint-danger {
  background: var(--el-color-danger);
}

.el-step__icon.is-text {
  border: 0;

}

.el-step__icon {
  display: inherit;
  font-size: 20px;
  height: 20px;
  width: 20px;
  cursor: pointer;
}

</style>