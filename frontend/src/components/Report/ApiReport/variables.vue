<template>
  <el-row>
    <el-col :span="8">
      <div>环境变量</div>
      <json-view v-if="envVariables" v-model:data="envVariables"></json-view>
    </el-col>
    <el-col :span="8">
      <div>用例变量</div>
      <json-view v-if="variables" v-model:data="variables"></json-view>
    </el-col>
    <el-col :span="8">
      <div>会话变量</div>
      <json-view v-if="sessionVariables" v-model:data="sessionVariables"></json-view>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted, reactive, toRefs, watch} from 'vue';
import jsonView from "/@/components/jsonView/index.vue";


export default defineComponent({
  name: 'extracts',
  components: {jsonView},
  props: {
    data: Object
  },
  emits: ['update:data'],
  setup(props: any) {
    const state = reactive({
      // data
      variables: {},
      globalVariables: {},
      envVariables: {},
      sessionVariables: {}
    });

    const initData = () => {
      state.variables = props.data.variables
      state.globalVariables = props.data.variables
      state.envVariables = props.data.envVariables
      state.sessionVariables = props.data.sessionVariables
    }

    onMounted(() => {
      nextTick(() => {
        initData()
      })
    })

    watch(
        () => props.data,
        () => {
          initData()
        },
        {deep: true}
    )

    return {
      ...toRefs(state)
    };
  },
});
</script>

<style lang="scss" scoped>

</style>