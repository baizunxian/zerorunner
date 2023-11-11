<template>
    <el-table
      class="ui-case-step"
      v-model:data="stepData"
      rowKey="index"
      ref="tableRef">

    <el-table-column width="40" align="center">
      <template #default="">
        <div class="move" style="cursor: all-scroll">
          <el-icon class="step-rank">
            <Rank></Rank>
          </el-icon>
        </div>
      </template>
    </el-table-column>

    <el-table-column type="expand" width="30">
      <template #default="{row}">
        <div style="padding: 0 30px">
          <z-monaco-editor style="height: 200px"
                           lang="python"
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
                     @change="(value) => pageElementChange(value, row)"
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
                     @change="(value) => {
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

    <el-table-column prop="data" label="" width="250px">
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

<script setup name="EditPage">
import {ElButton, ElCascader, ElCheckbox, ElInput} from "element-plus";
import {h, nextTick, onMounted, reactive, ref} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import {Bottom, CirclePlus, Rank, RefreshLeft, Top} from "@element-plus/icons"
import MonacoEditor from "/@/components/monaco/index.vue";
import Sortable from "sortablejs";
import useVModel from "/@/utils/useVModel";

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
      render: ({row}) => h(Rank, {}),
    },
    {
      key: 'script', prop: 'script', label: '', columnType: 'expand', width: '30', show: true,
      render: ({row}) => h(MonacoEditor, {
        value: row.script,
        lang: 'python',
        style: {
          height: '200px',
          width: '100%',
          margin: '0 30px',
        },
        "onUpdate:value": (val) => {
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
      render: ({row}) => h(ElCheckbox, {
        modelValue: row.enable,
      }),
    },
    {
      key: 'name', label: '步骤名称', prop: 'name', align: 'center', show: true,
      render: ({row}) => h(ElInput, {
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
      render: ({row}) => h(ElCascader, {
        modelValue: row.page_element_id,
        options: state.pageElementList,
        style: {width: '100%'},
        onChange: (value) => {
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
      render: ({row}) => h(ElCascader, {
        modelValue: row.action_value,
        options: state.actions,
        onChange: (value) => {
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
      render: ({row}) => h(ElInput, {
        modelValue: row.data,
        placeholder: '请输入数据',
        clearable: true,
      }),
    },
    {
      label: '操作', fixed: 'right', width: '', align: 'center',
      render: ({row, $index}) => h("div", null, [
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

const stepData = useVModel(props, 'stepDataList', emit)


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


const copyCaseStep = (row) => {
  console.log(row, 'row')
  let newRow = JSON.parse(JSON.stringify(row))
  stepData.value.push(newRow)
  // state.stepDataList.push(stepData)
}

const deletedCaseStep = (index) => {
  // state.stepDataList.splice(index, 1)
  stepData.value.splice(index, 1)
}

const handelBreakpoint = (row) => {
  row.breakpoint = !row.breakpoint
}

// 计算index，保持拖动后顺序
const computeDataIndex = (data) => {
  if (data) {
    data.forEach((data, index) => {
      data.index = index + 1
    })
  }
}

// pageElementChange
const pageElementChange = (value, row) => {
  row.page_id = row.page_element_id ? row.page_element_id[0] : ''
  row.element_id = row.page_element_id ? row.page_element_id[1] : ''
  let pageInfo = state.pageElementList.find((item) => item.id === row.page_id)
  console.log(pageInfo, 'pageInfo')
  if (pageInfo && pageInfo.elements) {
    let elementInfo = pageInfo.elements.find((item) => item.id === row.element_id)
    if (elementInfo) {
      row.location_method = elementInfo.location_method
      row.location_value = elementInfo.location_value
    }
  }
}

// 移动数据
const moveStep = (index, type) => {
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
  const el = tableRef.value.$el.querySelector('.ui-case-step .el-table__body-wrapper tbody')
  if (el) {
    Sortable.create(el, {
      animation: 200,
      sort: true,
      handle: ".move",
      fallbackClass: "custom-fallback-class",
      forceFallback: true,
      onEnd: ({newIndex, oldIndex}) => {
        let newStepData = stepData.value
        const currRow = newStepData.splice(oldIndex, 1)[0]
        newStepData.splice(newIndex, 0, currRow)
        nextTick(() => {
          stepData.value = [...newStepData]
          computeDataIndex(stepData.value)
        })
      }
    });

  }

}

onMounted(() => {
  getAllPageElement()
  createSortable()
})

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

<style>

@-webkit-keyframes drag-custom-fallback-class {
  0% {
    opacity: 0.7;
  }
  50% {
    opacity: 0.3;
  }
  100% {
    opacity: 0.7;
  }
}

@keyframes drag-custom-fallback-class {
  0% {
    opacity: 0.7;
  }
  50% {
    opacity: 0.3;
  }
  100% {
    opacity: 0.7;
  }
}

/* 定义自定义fallbackClass的样式 */
.custom-fallback-class {
  -webkit-animation: drag-custom-fallback-class 0.7s infinite;
  animation: drag-custom-fallback-class 0.7s infinite;
  background-color: lightyellow; /* 背景颜色为淡黄色 */
  border: 2px dashed orange; /* 边框为橙色虚线 */
  opacity: 0.5; /* 透明度为50% */
  cursor: grab; /* 光标为手型 */
}
</style>