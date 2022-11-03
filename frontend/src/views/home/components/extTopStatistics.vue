<template>
  <el-card class="box-card" style="height: 100%; margin-right: 8px" ref="cardRef">
    <div ref="echartsRef" :style="{height: `${height}px`}"></div>
  </el-card>
</template>

<script>
import * as ECharts from 'echarts'
import light from 'echarts/lib/theme/light.js'
import {defineComponent, markRaw, nextTick, onMounted, reactive, ref, toRefs, watch} from "vue";

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
      let usernameList = []
      let runNumList = []

      if (props.data.length > 0) {
        props.data.forEach(e => {
          usernameList.push(e.username)
          runNumList.push(e.run_num)
        })
      }
      state.echartsInfo = markRaw(ECharts.init(echartsRef.value))
      state.echartsInfo.setOption({
        title: {
          text: '执行统计',
          textStyle: {
            color: '#000000',
            fontSize: 14,
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },

        legend: {},
        grid: {
          left: '4%',
          right: '4%',
          bottom: '4%',
          top: '15%',
          containLabel: true
        },
        axisLabel: {
          interval: 0,
          // rotate: 45, //代表逆时针旋转45度
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01],
          axisTick: {
            alignWithLabel: true
          },

        },
        yAxis: {
          type: 'category',
          data: usernameList.reverse(),
          axisLabel: {
            interval: 0
          }
        },
        series: [
          {
            type: 'bar',
            barWidth: 20,
            label: {
              show: true,
              fontSize: 10,
            },
            data: runNumList.reverse()
          }
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