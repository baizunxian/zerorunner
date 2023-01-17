<template>
  <draggable
      class="dragArea"
      :list="tasks"
      tag="div"
      @start="true"
      @end="false"

      :group="{ name: 'g1' }"
      item-key="id"
  >
    <template #item="{ element }">
      <div>
        <div class="el-card" style="margin: 10px">
          <span>{{ element.name }}</span>
          <nested-draggable :tasks="element.step_data"/>
        </div>
      </div>

    </template>
  </draggable>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import draggable from 'vuedraggable'

export default defineComponent({
  name: 'nested-draggable',
  components: {
    draggable,
  },
  props: {
    tasks: {
      required: true,
      type: Array
    }
  },
  emits: ['update:tasks'],
});
</script>

<style lang="scss">
.dragArea {
  min-height: 50px;
  //background-color: #caced0;
  //border: 1px solid #1f1f1f;
  //outline: 1px dashed !important;
}

//ul {
//  display: block;
//  list-style-type: disc;
//  margin-block-start: 1em;
//  margin-block-end: 1em;
//  margin-inline-start: 0px;
//  margin-inline-end: 0px;
//  padding-inline-start: 40px;
//}

</style>