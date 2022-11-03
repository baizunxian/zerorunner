<template>
  <el-card class="box-card" style="height: 100%; margin-right: 8px" ref="cardRef">
    <div ref="echartsRef" :style="{height: `${height}px`}"></div>
  </el-card>
</template>

<script>
import * as ECharts from 'echarts'
import light from 'echarts/lib/theme/light.js'
import {defineComponent, markRaw, onMounted, reactive, ref, toRefs, watch} from "vue";

ECharts.registerTheme('ovilia-green', light) //引入主题
export default defineComponent({
  name: 'runTrend', //运行趋势
  props: {
    data: Object
  },

  setup(props) {
    const echartsRef = ref()
    const cardRef = ref()
    const state = reactive({
      height: 0,
      echartsInfo: null,
    });

    const initData = () => {
      state.echartsInfo = markRaw(ECharts.init(echartsRef.value))
      state.echartsInfo.setOption({
        title: {
          text: '运行趋势',
          textStyle: {
            color: '#000000',
            fontSize: 14,
          },
        },
        tooltip: {
          confine: true,
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['模块', '用例', '套件']
        },
        toolbox: {
          feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '4%',
          top: '15%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: props.data.date,
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '总执行数',
            type: 'line',
            stack: '总执行数',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: props.data.run_count
          },
          {
            name: '模块',
            type: 'line',
            stack: '模块',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: props.data.module_exe_num
          },
          {
            name: '用例',
            type: 'line',
            stack: '用例',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: props.data.case_exe_num
          },
          {
            name: '套件',
            type: 'line',
            stack: '套件',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: props.data.suite_exe_num
          }
        ]
      })

    };
    watch(
        () => props.data,
        (val) => {
          if (val) initData()
        }, {
          deep: true
        }
    );
    const initEchartsResizeFun = () => {
      state.echartsInfo?.resize()
    };
    onMounted(() => {
      state.height = cardRef.value.$el.offsetHeight * 0.9
      window.addEventListener('resize', initEchartsResizeFun)
    })
    return {
      initData,
      echartsRef,
      cardRef,
      ...toRefs(state),
    };
  }
});

</script>

<style lang="scss" scoped>
:deep(.el-card__body) {
  padding: 0;
}

</style>