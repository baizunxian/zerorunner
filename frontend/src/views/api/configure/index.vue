<template>
  <div id="minder-container">

  </div>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, toRefs} from 'vue';
// import * as kity from "kity"
// import * as kityminder from "kityminder-core"
//
// window.kity = kity


export default defineComponent({
  name: 'apiConfigure',
  components: {},
  setup() {
    const state = reactive({
      kityminder: null,
    });
    // 初始化表格数据

    const initMinder = () => {
      // window.kityminder = kityminder
      state.kityminder = window.kityminder = new kityminder.Minder();
      state.kityminder.setup('#minder-container');
      // state.kityminder = kityminder.Minder({
      //   renderTo: '#minder-container'
      // })
      state.kityminder.importJson({
        "root": {
          "data": {
            "text": "test111"
          },
          "children": [
            {"data": {"text": "新闻\nsrc/module/node.j"}},
            {"data": {"text": "网页"}},
            {"data": {"text": "贴吧"}},
            {"data": {"text": "知道"}},
            {"data": {"text": "音乐"}},
            {"data": {"text": "图片"}},
            {"data": {"text": "视频"}},
            {"data": {"text": "地图"}},
            {"data": {"text": "百科", "expandState": "collapse"}}
          ]
        },
        "template": "default"
      });
    }

    // 页面加载时
    onMounted(() => {
      nextTick(() => {
        initMinder()

      })
    });
    return {

      ...toRefs(state),
    };
  },
});
</script>
