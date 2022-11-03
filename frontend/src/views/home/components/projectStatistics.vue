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
  name: 'extTop', // 执行排行
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
      let module_list = []
      let successes_rate_list = []
      let pass_rate_list = []
      props.data.forEach(e => {
        module_list.push(e.project_name)
        successes_rate_list.push(e.successes_rate ? e.successes_rate : 0)
        pass_rate_list.push(e.pass_rate ? e.pass_rate : 0)
      })

      state.echartsInfo = markRaw(ECharts.init(echartsRef.value))
      state.echartsInfo.setOption({
        tooltip: {
          confine: true,
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        title: {
          text: '产品数据统计',
          textStyle: {
            color: '#000000',
            fontSize: 14,
          },
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '4%',
          top: '15%',
          containLabel: true
        },
        legend: {
          data: ['成功率', '通过率', '覆盖率']
        },
        toolbox: {
          show: true,
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: module_list,
            axisLabel: {
              interval: 0,
              formatter: function (params, index) {
                if (index % 2 !== 0) {
                  return '\n\n' + params
                } else {
                  return params
                }
              },
              textStyle: {
                fontSize: '10'
              }
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisLabel: {
              show: true,
              interval: 'auto',
              formatter: '{value}%'
            },
          }
        ],
        series: [
          {
            name: '成功率',
            type: 'bar',
            barWidth: 20,
            emphasis: {
              focus: 'series'
            },
            data: successes_rate_list
          },
          {
            name: '通过率',
            type: 'bar',
            barWidth: 20,
            emphasis: {
              focus: 'series'
            },
            data: pass_rate_list
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