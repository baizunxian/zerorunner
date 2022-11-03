<template>
  <el-card class="box-card h100" style="margin-right: 8px;" ref="cardRef">
    <el-tabs v-model="activeName">
      <el-tab-pane label="项目用例数TOP" name="first" class="h100">
        <div ref="pcnsRef" id="pcns">
          <el-table
              class="h100"
              :data="data.pcns_data"
              stripe
              :max-height="tableHeight"
              :show-header="false"
          >
            <el-table-column
                prop="name"
                label="项目"
                width="auto">
              <template #default="{row, $index}">
                <div class="top-content">
                  <SvgIcon class="top-row" v-if="$index === 0" :name="gold_medal"/>
                  <SvgIcon class="top-row" v-if="$index === 1" :name="silver_medal"/>
                  <SvgIcon class="top-row" v-if="$index === 2" :name="bronze_medal"/>
                  <span class="top-row">{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column
                prop="case_num"
                align="right"
                label="用例总数">
              <template #default="{row}">
                {{ row.case_num }}条
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
      <el-tab-pane label="用例创建TOP" name="second">

        <el-table
            :data="data.ucns_data"
            stripe
            :max-height="tableHeight"
            :show-header="false"
            style="width: 100%">
          <el-table-column
              prop="username"
              label="创建人"
              width="auto">
            <template #default="{row, $index}">
              <div class="top-content">

                <SvgIcon class="top-row" style="font-size: 18px;" v-if="$index === 0" :name="gold_medal"/>
                <SvgIcon class="top-row" style="font-size: 18px;" v-if="$index === 1" :name="silver_medal"/>
                <SvgIcon class="top-row" style="font-size: 18px;" v-if="$index === 2" :name="bronze_medal"/>
                <span class="top-row">{{ row.username }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column
              prop="case_num"
              align="right"
              label="用例总数">
            <template #default="{row, $index}">
              <span :title="$index">{{ row.case_num }}条</span>

            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <!--      <el-tab-pane label="角色管理" name="third">角色管理</el-tab-pane>-->
      <!--      <el-tab-pane label="定时任务补偿" name="fourth">定时任务补偿</el-tab-pane>-->
    </el-tabs>
  </el-card>

</template>


<script lang="ts">
import {computed, defineComponent, reactive, ref, toRefs} from 'vue';
import gold_medal from "/@/icons/indexSvg/gold_medal.svg";
import silver_medal from "/@/icons/indexSvg/silver_medal.svg";
import bronze_medal from "/@/icons/indexSvg/bronze_medal.svg";

export default defineComponent({
  name: 'top',
  props: {
    data: Object
  },
  setup() {
    const cardRef = ref()
    const pcnsRef = ref()
    const state = reactive({
      activeName: 'first',
    });

    const tableHeight = computed(() => {
      return window.innerHeight - (window.innerHeight * 0.7) - 100
    })
    return {
      cardRef,
      pcnsRef,
      tableHeight,
      gold_medal,
      silver_medal,
      bronze_medal,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-card__body ) {
  padding: 0 5px;
  height: 100%;
}

:deep(.el-tabs__content) {
  height: 100%;
}

.box-card {
  padding: 0 5px;
}

:deep(.el-tabs__header) {
  margin: 0 0 8px;
}

:deep(.el-tabs__item.is-active) {
  color: #000000;
  font-weight: 600;
}

.top-content {
  vertical-align: middle;
  box-sizing: border-box;
  display: block;

  .top-row {
    display: inline-block;
    box-sizing: border-box;
    vertical-align: middle;
  }
}


</style>