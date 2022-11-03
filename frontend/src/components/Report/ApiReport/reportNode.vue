<template>
  <div style="width: calc(100% - 20px);">
    <el-card style="width: 100%; height: 100%;" class="zero-base-card">
      <div class="zero-base-header">
        <!--步骤-->
        <div class="el-step__icon is-text">
          <div class="el-step__icon-inner">{{ data.index }}</div>
        </div>
        <svg-icon :name="data.showDetail ? 'ele-ArrowDown' : 'ele-ArrowRight'"
                  style="height: 20px; width: 20px"></svg-icon>

        <span>{{ data.name }}</span>
        <div class="header-right">
          <el-tag :type="data.success ? 'success' : 'danger'">
            {{ data.success ? "成功" : "失败" }}
          </el-tag>
          <span @click.stop="">
            <el-tooltip content="启用/禁用" placement="top">
              <el-switch
                  v-model="data.success"
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

        <report-detail :data="data?.step_datas?.data"></report-detail>

      </div>
    </el-card>
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import reportDetail from "/@/components/Report/ApiReport/reportDetail.vue";

export default defineComponent({
  name: 'reportNode',
  components: {
    reportDetail,
  },
  props: {
    data: Object,
  },
  emits: ['update:data', "copy-node", "deleted-node"],
  setup(props, {emit}) {


    return {}
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