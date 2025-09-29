<template>
  <el-dialog
      draggable
      v-model="state.showDialog"
      width="800"
      class=""
      destroy-on-close
      :close-on-click-modal="false">
    <template #header>
      <strong>新增步骤</strong>
    </template>
    <div class="create-step-box">
      <el-row :gutter="60">
        <el-col :span="8" v-for="step in state.stepTypeList" :key="step">
          <el-card class="step-item" shadow="hover" :style="step.style" @click="createStep(step.stepType)">
            <div class="step-icon">
              <StepIcon :step-type="step.stepType" :size="'40px'"></StepIcon>
            </div>
            <div class="step-name">
              {{ step.name }}
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </el-dialog>

</template>

<script setup lang="ts" name="createStep">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { getStepTypeInfo , stepTypeEnum} from "/@/utils/case.js";
import StepIcon from "/@/components/Z-StepController/StepIcon.vue"


const router = useRouter()
const state = reactive({
  formData: {
    curl_content: '',
    import_type: 'cURL',
  },
  activeType: null ,
  fileList: [],
  showDialog: false,
  stepTypeList: [
    {
      name: '新增接口步骤',
      icon: getStepTypeInfo(stepTypeEnum.Api, 'icon'),
      style: getStepTypeInfo(stepTypeEnum.Api, 'style'),
      stepType: 'api'
    },
    {
      name: '新增SQL步骤',
      icon: getStepTypeInfo(stepTypeEnum.Sql, 'icon'),
      style: getStepTypeInfo(stepTypeEnum.Sql, 'style'),
      stepType: 'sql',
    },
    {
      name: '新增PyScript步骤',
      icon: getStepTypeInfo(stepTypeEnum.Script, 'icon'),
      style: getStepTypeInfo(stepTypeEnum.Script, 'style'),
      stepType: 'script',
    },
    // {name: 'Jmeter', icon: jmeterImg, remarks: "支持 <div class='el-tag'>jmx</div> 数据格式。"},
  ]
})

const createStep = (stepType: string) => {
  router.push({ name: 'EditApiInfo', query: { stepType: stepType, timestamp: new Date().getTime() } })
  state.showDialog = false
}

const onOpen = () => {
  state.showDialog = true
}

defineExpose({
  onOpen
})

</script>


<style scoped lang="scss">
.create-step-box {
  min-height: 50vh;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 35px;

  .step-item {
    width: 180px;
    height: 240px;
    margin: auto;
    cursor: pointer;

    .step-icon {
      height: 150px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: auto;
      border-radius: 999px;

      i {
        font-size: 40px;
      }
    }

    .step-name {
      height: 50px;
      line-height: 50px;
      text-align: center;

    }

  }
}
</style>