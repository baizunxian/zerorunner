<template>
  <el-card class="box-card h100" style="margin-right: 8px;">
    <el-tabs v-model="activeName">
      <el-tab-pane label="项目套件数" name="first" class="h100">
        <el-table
            class="h100"
            :data="data.scns_data"
            stripe
            :max-height="tableHeight"
            :show-header="false"
        >
          <el-table-column
              prop="name"
              label="项目"
              width="auto">
            <template #default="{row, $index}">
              <svg-icon style="font-size: 18px;" v-if="$index === 0" class-name="gold_medal" icon-class="gold_medal"/>
              <svg-icon style="font-size: 18px;" v-if="$index === 1" class-name="silver_medal"
                        icon-class="silver_medal"/>
              <svg-icon style="font-size: 18px;" v-if="$index === 2" class-name="bronze_medal"
                        icon-class="bronze_medal"/>
              {{ row.name }}
            </template>
          </el-table-column>

          <el-table-column
              prop="case_num"
              align="right"
              label="套件数">
            <template #default="{row, $index}">
                <span v-if="$index === 0">
                  <svg-icon class-name="search-icon" icon-class="gold_modal"/>
                </span>
              {{ row.case_num }}个
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-card>

</template>


<script lang="ts">
import {computed, defineComponent, reactive, toRefs} from 'vue';


export default defineComponent({
  name: 'suiteTop',
  props: {
    data: Object
  },
  setup() {
    const state = reactive({
      activeName: 'first',
    });
    const tableHeight = computed(() => {
      return window.innerHeight - (window.innerHeight * 0.7) - 100
    })
    return {
      tableHeight,
      ...toRefs(state),
    };
  },
});
</script>

<style lang="scss" scoped>
:deep(.el-card__body ) {
  padding: 0 5px;
  height: 100%;
}

:deep(.el-tabs__content) {
  height: 100%;
}

.box-card {
  padding: 0 5px;
}

:deep(.el-tabs__header) {
  margin: 0 0 8px;
}

:deep(.el-tabs__item.is-active) {
  color: #000000;
  font-weight: 600;
}

</style>