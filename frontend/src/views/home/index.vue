<template>
  <div class="home-container" style="height: 100%;">
    <svg-icon icon-class="bug" />

    <el-row style='margin-bottom: 10px' :gutter="35">
      <el-col :span='24' class='common'>
        <count-statistics :data="countInfo" />
      </el-col>
    </el-row>

    <!--    top, 运行分析-->
    <el-row style='margin-bottom: 10px ; height: 30%'>
      <el-col :span='6' class='common' style="max-height: 100%">
        <case-top-statistics :data='topInfo'/>
      </el-col>
      <el-col :span='18' class='common'>
        <project-statistics :data="projectRate"></project-statistics>
      </el-col>
    </el-row>

    <el-row style='height: 30%; margin-bottom: 10px'>
      <el-col :span='6' class='common' style="max-height: 100%">
        <suite-top-statistics :data="topInfo" />
      </el-col>
      <el-col :span='18' class='common'>
        <ext-trend-statistics :data='caseRunInfo'/>
      </el-col>
    </el-row>

    <el-row style='height: 30%; margin-bottom: 10px'>
      <el-col :span='6' class='common' style="max-height: 100%">
        <ext-top-statistics :data='reportInfo'/>
      </el-col>
      <el-col :span='18' class='common'>
        <run-trend-statistics :data='caseRunInfo'/>
      </el-col>
    </el-row>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs} from 'vue';
import CountStatistics from '/@/views/home/components/countStatistics.vue';
import ProjectStatistics from '/@/views/home/components/projectStatistics.vue';
import SuiteTopStatistics from '/@/views/home/components/suiteTopStatistics.vue';
import CaseTopStatistics from '/@/views/home/components/caseTopStatistics.vue';
import ExtTopStatistics from '/@/views/home/components/extTopStatistics.vue';
import RunTrendStatistics from '/@/views/home/components/runTrendStatistics.vue';
import ExtTrendStatistics from '/@/views/home/components/extTrendStatistics.vue';
import {useStatisticsApi} from "/@/api/useSystemApi/statistic";

export default defineComponent({
  name: 'home',
  components: {
    CountStatistics,
    ProjectStatistics,
    SuiteTopStatistics,
    CaseTopStatistics,
    ExtTopStatistics,
    ExtTrendStatistics,
    RunTrendStatistics,
  },
  setup() {
    const state = reactive({
      countInfo: {},
      topInfo: {},
      projectRate: null,
      reportInfo: null,
      caseRunInfo: null,
    });
    const initData = () => {
      useStatisticsApi().countStatistic()
          .then((res: any) => {
            state.countInfo = res.data.count_info
            state.projectRate = res.data.project_rate
            state.topInfo = res.data.top_info
            state.reportInfo = res.data.report_info
            state.caseRunInfo = res.data.case_run_info
          })
    }
    onMounted(() => {
      initData()
    })
    return {
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

.home-container {
  padding: 15px;
}

</style>