<template>

  <div>
    <div style="display: flex; width: 100%; justify-content: space-between">
      <el-select
          v-model="state.env_id"
          placeholder="选择运行环境"
          filterable style="width: 30%;">
        <el-option
            v-for="env in state.envList"
            :key="env.id + env.name"
            :label="env.name"
            :value="env.id">
          <span style="float: left">{{ env.name }}</span>
        </el-option>
      </el-select>
      <el-button type="primary" @click="state.showCasePage =!state.showCasePage">选择用例</el-button>
    </div>
    <z-table
        :columns="state.caseColumns"
        :data="state.caseList"
        :show-page="false"
        :border="false"
        row-key="id"
    ></z-table>

    <el-dialog
        draggable
        title="选择用例"
        v-model="state.showCasePage"
        width="80%">
      <SelectCase ref="selectCaseRef"></SelectCase>
      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addCase">添加</el-button>
      </span>
      </template>
    </el-dialog>

  </div>

</template>

<script setup name="TaskCaseInfo">
import SelectCase from "/@/components/Z-StepController/caseInfo/SelectCase.vue"


import {h, onMounted, reactive, ref, watch} from "vue";
import {ElButton} from "element-plus";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {useApiCaseApi} from "/@/api/useAutoApi/apiCase";

const props = defineProps({
  caseIds: {
    type: Array,
    default: () => []
  },
  envId: {
    type: Number,
  }
})


const selectCaseRef = ref()

const state = reactive({
  showCasePage: false,
  env_id: null,
  caseList: [],
  caseColumns: [
    {label: '序号', columnType: 'index', width: 'auto', show: true},
    {key: 'name', label: '用例名称', width: '', align: 'center', show: true},
    {key: 'remarks', label: '用例描述', width: '', align: 'center', show: true},
    {
      label: '操作', columnType: 'string', fixed: 'right', width: '80', align: 'center',
      render: (row, index) => h("div", null, [
        //
        // h(ElButton, {
        //   type: "primary",
        //   onClick: () => {
        //   }
        // }, () => '编辑'),

        h(ElButton, {
          type: "danger",
          onClick: () => {
            deletedCase(index)
          }
        }, () => '删除')
      ])
    },
  ],
  // env
  envList: [],
  envQuery: {
    page: 1,
    pageSize: 1000
  },
})


const initData = () => {
  console.log("props---", props)
  state.env_id = props.envId
  useApiCaseApi().getCaseByIds({ids: props.caseIds})
      .then(res => {
          state.caseList = res.data.length? res.data : []
      })
}


// env
const getEnvList = () => {
  useEnvApi().getList(state.envQuery)
      .then(res => {
        state.envList = res.data.rows
      })
};


/*添加用例*/
const addCase = () => {
  let selectCaseData = selectCaseRef.value.getSelectionData()
  if (selectCaseData) {
    selectCaseData.forEach((caseInfo) => {
      if (state.caseList) {
        let existCaseInfo = state.caseList.find((e) => e.id == caseInfo.id)
        if (!existCaseInfo) {
          state.caseList.push(caseInfo)
        }
      }
    })
  }
  state.showCasePage = false
}
/*删除用例*/
const deletedCase = (index) => {
  state.caseList.splice(index, 1)
}

const getCaseEnvId = () => {
  return state.env_id
}


const getCaseIds = () => {
  let caseIds = []
  state.caseList.forEach((c) => {
    caseIds.push(c.id)
  })
  return caseIds
}


watch(
    () => props.envId,
    (val) => {
      initData()
    }, {
      deep: true
    }
);

watch(
    () => props.caseIds,
    (val) => {
      initData()
    }, {
      deep: true
    }
);


// 页面加载时
onMounted(() => {
  initData()
  getEnvList();
});

defineExpose({
  getCaseEnvId,
  getCaseIds,
  initData,
})

</script>

<style scoped>

</style>