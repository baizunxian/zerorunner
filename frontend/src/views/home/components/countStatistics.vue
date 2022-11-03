<template>
  <div class="h100">
    <el-row class="h100">
      <el-col :span="4" class="common" v-for="(tool, index) in list" :key="index">
        <div class="item" @click="clickToPage(tool.full_path)">
          <SvgIcon :name="tool.icon" :size="34"/>
          <div class="item__content">
            <span class="title" :id="tool.key">{{ data[tool.key] }}</span>
            <span class="remark">{{ tool.name }}</span>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs, watch} from 'vue';
import project_svg from "/@/icons/indexSvg/project_svg.svg";
import module_svg from "/@/icons/indexSvg/module_svg.svg";
import case_svg from "/@/icons/indexSvg/case_svg.svg";
import suite_svg from "/@/icons/indexSvg/suite_svg.svg";
import exc_count from "/@/icons/indexSvg/exc_count.svg";
import add_case from "/@/icons/indexSvg/add_case.svg";
import logoMini from '/@/assets/login-icon-two.svg';
import CountUp from 'countup';

export default defineComponent({
  name: 'countStatistics',
  props: {
    data: Object
  },
  setup(props: any) {
    const state = reactive({
      list: [
        {name: '项目', key: 'project_count', icon: project_svg},
        {name: '模块', key: 'module_count', icon: module_svg},
        {name: '用例', key: 'case_count', icon: case_svg},
        {name: '套件', key: 'suite_count', icon: suite_svg},
        {name: '当天运行用例数', key: 'today_run_count', icon: exc_count},
        {name: '当天用例新增数', key: 'add_case_count', icon: add_case}
      ],
    });

    const countUp = () => {
      state.list.forEach(e => {
        new (CountUp as any)(e.key, 0, props.data[e.key] ? props.data[e.key] : 0).start()
      })
    }

    watch(
        () => props.data,
        (val) => {
          if (val) countUp()
        }
    );
    return {
      project_svg,
      module_svg,
      case_svg,
      suite_svg,
      exc_count,
      add_case,
      logoMini,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
.box-card {
  margin: 10px;
  height: calc(100% - 20px);
}

.item {
  border-radius: 5px;
  width: 95%;
  float: left;
  display: flex;
  align-items: center;
  height: 60px;
  padding-left: 16px;
  border: 1px solid #EBEEF5;
  background-color: #FFF;
  color: #303133;
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
  //margin-left: 16px;
  //margin-top: 16px;

  &:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .5);
  }

  &__content {
    display: flex;
    flex-direction: column;
    margin-left: 16px;
  }

  .icon {
    font-size: 32px;
  }

  .title {
    font-size: 20px;
    color: #333333;
    font-weight: 600;
  }

  .remark {
    font-size: 12px;
    color: #999999;
  }
}

.wiki {
  background-color: #e7faf0;
}

:deep(.el-card__header) {
  padding: 10px 10px;
}

:deep(.el-card__body) {
  padding: 0;
}

:deep(.el-checkbox__label) {
  width: 100px;
}
</style>
