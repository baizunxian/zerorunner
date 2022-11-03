<template>
  <div style="width: calc(100% - 20px);">
    <el-card style="width: 100%; height: 100%;" class="zero-base-card">
      <div class="zero-base-header">
        <!--步骤-->
        <div class="el-step__icon is-text">
          <div class="el-step__icon-inner">{{ data.index }}</div>
        </div>
        <!--脚本类型-->
        <svg-icon :name="data.showDetail ? 'ele-ArrowDown' : 'ele-ArrowRight'"
                  style="height: 20px; width: 20px"></svg-icon>
        <!--        <svg-icon v-else name="ele-ArrowDown" style="height: 20px; width: 20px"></svg-icon>-->

        <el-tag style="margin: 0 5px" size="small">{{ optType[data.step_type] }}</el-tag>
        <!--脚本名称-->
        <template v-if="data.step_type === 'wait'">
          <el-input-number v-model="data.value" @click.stop=""/>
          <span>m</span>
        </template>

        <template v-else>
          <span v-if="!data.edit">
                <svg-icon name="ele-EditPen" @click.stop="editeName(data)"/>
                {{ data.name }}
          </span>
          <el-input v-else
                    :id="`editeName_${data.index}`"
                    v-model="data.name"
                    style="width: 200px;"
                    @click.stop.native=""
                    @blur="nameEditBlur(data)">
          </el-input>
        </template>


        <!--              操作-->
        <div class="header-right">
          <span @click.stop="">
            <el-tooltip content="启用/禁用" placement="top">
              <el-switch
                  v-model="data.enable"
                  inline-prompt>
              </el-switch>
            </el-tooltip>
          </span>

          <el-button circle style="margin-left: 5px" @click.stop="copyNode(data)">
            <el-icon>
              <ele-DocumentCopy/>
            </el-icon>
          </el-button>

          <el-button type="danger" circle @click.stop="deletedNode(data.index)">
            <el-icon>
              <ele-Delete/>
            </el-icon>
          </el-button>
        </div>

        <script-controller v-if="data.step_type === 'script'" v-model:data="data"/>
        <sql-controller v-if="data.step_type === 'sql'" v-model:data="data"/>
        <extract-controller v-if="data.step_type === 'extract'" v-model:data="data"/>
        <case-controller v-if="data.step_type === 'case'" v-model:data="data"/>

      </div>
    </el-card>
  </div>

</template>

<script lang="ts">
import {defineComponent, nextTick} from 'vue';
import scriptController from "/@/components/StepController/scriptController.vue";
import sqlController from "/@/components/StepController/sqlController.vue";
import extractController from "/@/components/StepController/extractController.vue";
import caseController from "/@/components/StepController/caseController.vue";

export default defineComponent({
  name: 'stepNode',
  components: {
    scriptController,
    sqlController,
    extractController,
    caseController,
  },
  props: {
    data: Object,
    optType: Object,
  },
  emits: ['update:data', "copy-node", "deleted-node"],
  setup(props, {emit}) {

    // 编辑脚本名称
    const editeName = (data: any) => {
      data.edit = true
      nextTick(() => {
        let inputRef = document.getElementById("editeName_" + data.index)
        if (inputRef) inputRef.focus();
      })
    }

    // 编辑失去焦点时触发
    const nameEditBlur = (data: any) => {
      data.edit = false
    }

    const copyNode = (data: any) => {
      emit("copy-node", data)
    }

    const deletedNode = (index: number) => {
      emit("deleted-node", index - 1)
    }

    return {
      editeName,
      nameEditBlur,
      copyNode,
      deletedNode,
    }
  },
});
</script>

<style lang="scss" scoped>
.zero-base-card {
  min-height: 36px;

  .zero-base-header {
    min-height: 26px;

    .el-tag--small {
      height: 24px;
    }

    .el-step__icon {
      width: 20px;
      height: 20px;
      font-size: 12px;
    }

    .header-right {
      //margin-top: 1px;
      float: right;
      z-index: 1;
    }
  }
}

</style>