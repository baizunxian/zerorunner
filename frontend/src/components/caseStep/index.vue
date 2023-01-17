<template>
  <div>
    <el-row>
      <el-col :span="12">
        <draggable
            v-model="apiList"
            :group="{ name: 'people', pull: 'clone', put: false }"
            @start="true"
            @end="false"
            item-key="id">
          <template #item="{element}">

            <div>{{ element.name }}</div>

          </template>
        </draggable>

      </el-col>
      <el-col :span="12">


        <nested-draggable :tasks="stepList"></nested-draggable>

        <pre>{{ stepList }}</pre>
      </el-col>
    </el-row>

  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, toRefs} from 'vue';
import draggable from 'vuedraggable'
import nestedDraggable from "/@/components/nestedDraggable/index.vue";
import {useApiInfoApi} from "/@/api/useAutoApi/apiInfo";

export default defineComponent({
  name: 'caseStep',
  components: {
    draggable,
    nestedDraggable,
  },
  props: {},
  emits: ['update:data'],
  setup(props: any) {
    const state = reactive({
      apiListQuery: {
        page: 1,
        pageSize: 10
      },

      // data
      apiList: [
        {name: "test1"},
        {name: "test2"},
        {name: "test3"},
        {name: "test4"},
      ],

      stepList: [
        {id: 1, name: "test5", step_data: [{id: 5, name: "step_data_1", step_data:[]}]},
        {id: 2, name: "test6", step_data: [{id: 6, name: "step_data_1", step_data:[]}]},
        {id: 3, name: "test7", step_data: [{id: 7, name: "step_data_1", step_data:[]}]},
        {id: 4, name: "test8", step_data: [{id: 8, name: "step_data_1", step_data:[]}]},
      ],


    });

    const getApiList = async () => {
      let {data} = await useApiInfoApi().getList(state.apiListQuery)
      state.apiList = data.rows
    }


    onMounted(() => {
      getApiList()
    })

    return {
      getApiList,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>

</style>