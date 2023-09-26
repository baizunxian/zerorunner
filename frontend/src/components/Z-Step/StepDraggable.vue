<template>
  <VueDraggableNext
      :list="data"
      handle=".handle"
      animation="200"
      :scroll-sensitivity="100"
      :force-fallback="true"
      :group="{ name: 'step', pull: checkPull , put: true}"
      fallback-class="shake"
      ghost-class="g-host"
      :move="onMove"
      chosen-class="move">
    <template #item="{element}">
      <div class="m10">
        <el-card>
          <el-button class="handle" circle size="small">
            <el-icon :size="13" style="vertical-align: middle">
              <Rank/>
            </el-icon>
          </el-button>
          {{ element.name }}
        </el-card>

        <StepDraggable v-if="element.sub_steps && element.sub_steps.length> 0"
                       :data="element.sub_steps"
                       style="padding-left: 10px"
        ></StepDraggable>
      </div>
    </template>
    <!--    <el-card v-for="step in stepData" :key="step">{{ element.name }}-->
    <!--      <el-button class="handle" circle size="mini">-->
    <!--        <el-icon :size="13" style="vertical-align: middle">-->
    <!--          <Rank/>-->
    <!--        </el-icon>-->
    <!--      </el-button>-->

    <!--      <StepDraggable :data="step.sub_steps"></StepDraggable>-->
    <!--    </el-card>-->
  </VueDraggableNext>
</template>

<script setup name="StepNode1">
import VueDraggableNext from 'vuedraggable'
import {Rank} from "@element-plus/icons"


const emit = defineEmits(['copy-node', 'deleted-node', "onUpdate:data"])

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  node: {
    type: Object,
  },
  optType: {
    type: Object,
  },
})


const onMove = () => {
  return true
}

const checkPull = (e) => {
  return true
}

</script>

<style lang="scss" scoped>

@-webkit-keyframes drag-shake {
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

@keyframes drag-shake {
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

.g-host {
  background: rgba(242, 246, 252, 0.7);
}

.shake {
  -webkit-animation: drag-shake 0.7s infinite;
  animation: drag-shake 0.7s infinite;
  border: 2px dashed #909399;
}

.move {
  border-radius: 10px;
}

.stepsTimeline {
  max-height: 75vh;
}
</style>