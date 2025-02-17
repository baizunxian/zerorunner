<template>
  <div>
    <el-card class="code-view-content">
      <pre class="source lang-java linenums" v-html="props.classContent" ref="codeContentRef"></pre>
    </el-card>
  </div>
</template>

<script setup name="codeView">
import '/@/theme/jacoco/prettify';
import '/@/theme/jacoco/prettify.css';
import '/@/theme/jacoco/report.css';
import {onMounted, reactive, ref, watch} from 'vue';

const codeContentRef = ref()

const props = defineProps({
  // java 类的内容
  classContent: {
    type: String,
    default: () => ''
  }
})
// 自定义数据
const state = reactive({
  breadcrumbs: [
    {name: "报告", el_type: 'report'},
  ],

});


const locationEl = (offset) => {
  window.prettyPrint()
  let element = codeContentRef.value.querySelector(`#L${offset}`)
  if (element) {
    element.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
  }
}

defineExpose({
  locationEl
})


// 页面加载时
onMounted(() => {
  // window['PR_TAB_WIDTH'] = 6;
  // window.prettyPrint()
});

watch(
    () => props.classContent,
    (val) => {
      if (val) {
        window.prettyPrint()
      }
    },
    {deep: true}
)


</script>

<style lang="scss" scoped>
.code-view-content {
  padding-left: 30px;
}

ol.L0 {
  list-style-type: space-counter;
}

:deep(pre.source li) {
  padding-left: 20px;
}

:deep(li .add-line::before) {
  position: absolute;
  padding-right: 8px;
  color: #1f883d;
  //top: 1px;
  left: 74px;
  content: "+ ";
}
</style>
