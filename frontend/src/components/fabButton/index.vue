<template>
  <div class="fab-main-container"
       id="fab"
       @click.stop="state.showMenu=!state.showMenu">
    <div class="fab-container fab fab-size-small">
      <div class="fabMask"></div>
      <i class="iconfont icon-add fab-container-icons" :class="[state.showMenu?'fab-active':'']"></i>
    </div>
    <transition name="breadcrumb">
      <div class="fab-item-container fab-size-small" v-show="state.showMenu">
        <div class="fab-container fab-item"
             v-for="(item, index) in value"
             :key="index"
             style="transition-delay: 0s;background: #F1EEE9FF;"
             :style="{top:`-${(index+1) * 30}px`,background: item.color, color: item.color, display: state.showMenu?'': 'none'}"
             @click.stop="item.func(item.param)"
        >
          <div class="fabMask" @click.stop="item.func(item.param)"></div>
          <div class="fab-item-title"
               :style="{color:item.color}"
               style="background: #FCF6EE;">
            {{ item.title }}
          </div>
          <div class="fab-item-image"></div>
          <i :class="item.icon" class="fab-icons" :style="{color:'#FFF'}"></i>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup name="z-fab">
import {reactive} from "vue";

const props = defineProps({
  value: {
    type: Array,
    default: () => []
  }
})

const state = reactive({
  // data
  showMenu: false,
});

const showMenu = () => {
  state.showMenu = !state.showMenu
}


defineExpose({
  showMenu
})

</script>

<style lang="scss" scoped>
.fab-container {
  transition-timing-function: linear;
  background: #409eff;
  box-shadow: #666666 0 2px 8px;
}

.fab-main-container {
  user-select: none;
  position: fixed;
  overflow: initial;
  box-sizing: border-box;

  .fab {
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 0;
    top: 0;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    padding: 8px;
    transition: all 0.2s linear;
  }

  .fab-size-small {
    height: 32px;
    width: 32px;
  }

  .fabMask {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    border-radius: 50%;
    background: #FFF;
    opacity: 0;
    transition: all .3s;
  }

  .fab-icons {
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.2s ease;
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    top: 0;
    font-size: 1em;
  }

  .fab-active {
    transform: rotate(45deg);
  }
}

#fab {
  right: 60px;
  bottom: 120px;
  z-index: 5;
}


// fab-item

.fab-item-container {
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  cursor: pointer;

  .fab-item {
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.2s linear;
    position: absolute;
    cursor: pointer;
    top: -50px;
    width: 80%;
    height: 80%;
    margin-left: 10%;
    border-radius: 50%;
    overflow: inherit;

    .fab-item-title {
      position: absolute;
      right: 4em;
      box-shadow: 0 1px 0.5px #ccc;
      padding: 2px 5px;
      font-size: .8em;
      min-width: 3em;
      white-space: nowrap;
      border-radius: 2px;
      text-align: center;
    }

    .fab-item-image {
      height: 100%;
      width: 100%;
      overflow: hidden;
    }
  }
}

.fab-container-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
  position: absolute;
  height: 100%;
  width: 100%;
  left: 0;
  top: 0;
  font-size: 1.5em;
}

.fab-enter-active,
.fab-leave-active {
  transition: opacity 0.8s ease;
}

.fab-enter {
  opacity: 0;
  transform: translate3D(0, 5px, 0) scale(0);
}

.fab-leave-to {
  opacity: 0;
}

</style>