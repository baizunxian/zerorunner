<template>
  <el-card class="box-card" style="height: 100%; margin-right: 8px" ref="cardRef">
    <div ref="echartsRef" :style="{height: `${height}px`}"></div>
  </el-card>
</template>

<script>
import * as ECharts from 'echarts'
import light from 'echarts/lib/theme/light.js'
import {defineComponent, markRaw, onActivated, onMounted, reactive, ref, toRefs, watch} from "vue";

ECharts.registerTheme('ovilia-green', light) //引入主题
export default defineComponent({
  name: 'extTrend',  // 执行趋势
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
      if (state.echartsInfo) state.echartsInfo.dispose()
      state.echartsInfo = markRaw(ECharts.init(echartsRef.value))
      state.echartsInfo.setOption({
        color: ['#67e0e3', '#f56c6c', '#ffdb5c'],
        title: {
          text: '执行趋势',
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
            crossStyle: {
              color: '#999'
            }
          },
        },
        toolbox: {
          feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        legend: {
          data: ['成功用例', '失败用例']
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
            data: props.data.date,
            boundaryGap: false,
            axisPointer: {
              type: 'shadow'
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            splitNumber: 5,
            axisLabel: {
              formatter: '{value}'
            }
          },

        ],
        series: [
          {
            name: '成功用例',
            type: 'line',
            stack: '1',
            barWidth: 30,
            data: props.data.pass
          },
          {
            name: '失败用例',
            type: 'line',
            stack: '2',
            barWidth: 30,
            data: props.data.fail
          },
        ]
      })
    };

    const initEchartsResizeFun = () => {
      state.echartsInfo?.resize()
    };

    watch(
        () => props.data,
        (val) => {
          if (val) initData()
        }
    );

    onActivated(() => {
      initEchartsResizeFun();
    });

    onMounted(() => {
      state.height = cardRef.value.$el.offsetHeight * 0.9
      window.addEventListener('resize', initEchartsResizeFun);
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