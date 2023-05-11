<template>
  <draggable
      class="dragArea"
      tag="div"
      :list="List"
      :group="{ name: 'description', put:()=> true, pull:true }"
      item-key="name"
      dragClass="dragClass"
      ghostClass="ghostClass"
      handle=".dragHandler"
  >
    <template #item="{ element }">
      <div class="blockWrapper">
        <div class="step-control-index-dndWrapper">
          <div class="dragHandler cursor-move">
            <span class="dragIcon">拖拽</span>
          </div>
          <div class="dndPreview">
            <div class="blockHeader">
              {{ element.name }}
            </div>
            <div class="droppableBox">
              <div class="relative">
                <nested-draggable v-if="element.sub_steps" :list="element.sub_steps"></nested-draggable>
              </div>
              <div class="droppableArea">拖入或</div>
            </div>
          </div>
        </div>

      </div>

    </template>
  </draggable>
</template>
<script setup lang="ts" name="nested-draggable">
import draggable from "vuedraggable";

const props = defineProps({
  List: {
    required: true,
    type: Array
  }
})

</script>


<style lang="scss" scoped>
.blockWrapper {
  position: relative;
  width: 100%;

  .step-control-index-dndWrapper {
    position: relative;
    padding-bottom: 6px;

    .dragHandler {

    }

    .dndPreview {
      //width: calc(100% - 360px);
      height: 100%;
      line-height: 1;
      background: var(--ant-component-background);
      --hover-border-color: rgba(86, 87, 88, 0.08);
      --open-border-color: rgba(154, 125, 86, 0.32);
      --draggable-border-color: rgba(154, 125, 86, 0.75);
      --open-border-bottom-color: rgba(86, 87, 88, 0.04);

      .blockHeader {
        display: flex;
        align-items: center;
        width: 100%;
        height: 100%;
        min-height: 40px;
        padding-right: 8px;
        white-space: nowrap;
        background: rgba(86, 87, 88, 0.04);
        border: 1px solid transparent;
        cursor: pointer;
        border-radius: 0;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        border-bottom-color: rgba(154, 125, 86, 0.32);
        border-color: rgba(154, 125, 86, 0.32);
      }

      .droppableBox {
        border: 1px solid transparent;
        padding: 12px;
        border-color: rgba(154, 125, 86, 0.32);
        border-style: solid;
        //border-width: 0 1px;
        //border-radius: 0;
        border-width: 0 1px 1px;
        border-radius: 0 0 4px 4px;

        .droppableArea {
          border: 1px dashed rgba(154, 125, 86, 0.32);
          padding-bottom: 6px;
          position: relative;
          width: 100%;
          height: 40px;
          color: var(--app-text-fg-low);
          line-height: 40px;
          text-align: center;
          border-color: rgba(86, 87, 88, 0.12);
          cursor: pointer;

        }

        .droppableArea:hover {
          border-color: rgba(154, 125, 86, 0.75)
        }
      }
    }
  }
}

.ghostClass {
  opacity: 0.8 !important;

  border: 5px solid saddlebrown;
}

.cursor-move {
  cursor: move;
}

.dragIcon {
  //position: absolute;
  top: 0;
  //left: -17px;
  width: 18px;
  height: 40px;
  color: var(--ui-text-color-secondary);
}
</style>