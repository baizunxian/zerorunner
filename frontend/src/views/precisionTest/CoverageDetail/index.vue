<template>
  <div class="app-container">
    <el-card class="coverage-report mb15">
      <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item
            v-for="(item, index) in state.breadcrumbs"
            @click="breadcrumbChange(item, index)"
            style="cursor: pointer"
            :style="getBackgroundImageStyle(item.el_type)"
            :key="item">
          <a href="" style="pointer-events: none; cursor: pointer">{{ item.name }}</a>
        </el-breadcrumb-item>
      </el-breadcrumb>
    </el-card>

    <el-card v-if="!state.showCodeViewPage" class="coverage-table">
      <!--      <template #header>{{ state.title }}</template>-->

      <z-table
          :columns="getColumns"
          :data="state.listData"
          ref="tableRef"
          :total="state.total"
          :show-page="false"
      >
      </z-table>

    </el-card>

    <CodeView v-if="state.showCodeViewPage" :classContent="state.classContent" class="coverage-code-view"
              ref="CodeViewRef"></CodeView>
  </div>
</template>

<script setup name="CoverageDetail">
import {computed, h, nextTick, onMounted, reactive, ref, watch} from 'vue';
import {ArrowRight} from '@element-plus/icons';
import {ElButton} from 'element-plus';
import packageGif from "/@/theme/jacoco/package.gif";
import classGif from "/@/theme/jacoco/class.gif";
import methodGif from "/@/theme/jacoco/method.gif";
import reportGif from "/@/theme/jacoco/report.gif";
import redbarGif from "/@/theme/jacoco/redbar.gif";
import greenbarGif from "/@/theme/jacoco/greenbar.gif";
import CodeView from "/src/views/precisionTest/CoverageDetail/codeView.vue";
import {useCoverageReportApi} from "/src/api/useCoverageApi/coverage";
import {useRoute} from "vue-router";


const route = useRoute()
// 自定义数据
const tableRef = ref();
const CodeViewRef = ref();
const state = reactive({
  title: "",
  breadcrumbs: [],
  currentBreadcrumb: null,
  baseColumns: [
    {label: '序号', columnType: 'index', align: 'center', width: 'auto', show: true},
    {
      key: 'name', label: '名称', align: 'left', width: '', show: true,
      render: ({row}) => h(ElButton, {
        link: true,
        type: "primary",
        style: getBackgroundImageStyle(row.el_type),
        onClick: () => {
          getCoverageDetail(row)
        }
      }, () => row.el_type !== 'method' ? row.name : row.name + row.params_string)
    },
    {
      key: 'instruction_covered', label: '指令覆盖率', align: 'center', width: '200', show: true,
      render: ({row}) => getCovRender(row, "instruction")
    },
    {
      key: 'branch_covered', label: '分支覆盖率', align: 'center', width: '200', show: true,
      render: ({row}) => getCovRender(row, "branch")
    },

    // {key: 'complexity_missed', label: '遗漏的cxty', align: 'center', width: '', show: true},
    {
      key: 'line_covered', label: '行覆盖率', align: 'center', width: '', show: true,
      render: ({row}) => h("span", null, `${row.line_covered}/${row.line_count}`)
    },
    {
      key: 'method_covered', label: '方法覆盖率', align: 'center', width: '', show: true,
      render: ({row}) => h("span", null, `${row.method_covered}/${row.method_count}`)
    },
  ],
  columns: [],
  listData: [],

  reportDetail: null,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },

  // code
  showCodeViewPage: false,
  classContent: ""
});

const getColumns = computed(() => {
  state.columns = [...state.baseColumns]
  let classColumn = {
    key: 'class_covered', label: '类覆盖率', align: 'center', width: '', show: true,
    render: ({row}) => h("span", null, `${row.class_covered}/${row.class_count}`)
  }
  if (state.currentBreadcrumb?.el_type !== 'class') {
    state.columns.push(classColumn)
  }
  return state.columns
})

const getCovRender = (row, column) => {
  const missed = row[`${column}_missed`]
  const count = row[`${column}_count`]
  let elList = [
    h("img", {
      style: {width: `${100 - getPercentage(missed, count)}%`, height: "10px"},
      src: greenbarGif,
      alt: ""
    }, ""),
    h("img", {
      style: {width: `${getPercentage(missed, count)}%`, height: "10px"},
      src: redbarGif,
      alt: ""
    }, ""),
    h("span", {
      style: {width: `40px`, textAlign: "end"},
    }, `${100 - getPercentage(missed, count)}%`),
  ]
  console.log("column", column, count)
  if (column == 'branch' && count === 0) {
    elList = [
      h("div", {
        style: {width: `100%`, height: "10px"},
        src: redbarGif,
        alt: ""
      }, ""),
      h("span", {
        style: {width: `40px`, textAlign: "end"},
      }, `n/a`),
    ]
  }

  return h("div", {
    title: `${count - missed}/${count}`,
    style: {
      width: "100%",
      height: "100%",
      margin: "0 auto",
      display: "flex",
      alignItems: "center",
      borderRadius: "8px",
    }
  }, elList)
}


const getCoverageDetail = async (row) => {
  let queryData = {
    report_id: row.report_id,
  }
  switch (row.el_type) {
    case "report":
      queryData.el_type = "report"
      state.breadcrumbs.push(row)
      break
    case "package":
      queryData.el_type = "package"
      queryData.package_name = row.package_name
      state.breadcrumbs.push(row)
      break
    case "class":
      queryData.el_type = "class"
      queryData.class_id = row.id
      state.breadcrumbs.push(row)
      break
    case "method":
      const classInfo = state.breadcrumbs.find(e => e.el_type === 'class')
      state.classContent = classInfo ? classInfo.class_file_content : ""
      state.breadcrumbs.push(row)
      break
    default:
      break
  }
  state.currentBreadcrumb = row
  state.showCodeViewPage = row.el_type === "method"
  if (state.showCodeViewPage) {
    await nextTick(() => {
      CodeViewRef.value.locationEl(row.offset)
    })
    return
  }
  let {data} = await useCoverageReportApi().getCoverageDetail(queryData)
  state.listData = data || []

}

const breadcrumbChange = (item, index) => {
  if (index === state.breadcrumbs.length - 1) {
    return
  }
  state.breadcrumbs = state.breadcrumbs.slice(0, index)
  getCoverageDetail(item)
}


// 获取百分比
const getPercentage = (missed, total) => {
  return missed === 0 ? 0 : Math.round(missed / total * 100)
}
// 获取背景图片
const getBackgroundImageStyle = (type) => {
  let imageUrl
  switch (type) {
    case "report":
      imageUrl = reportGif
      break
    case "package":
      imageUrl = packageGif
      break
    case "class":
      imageUrl = classGif
      break
    case "method":
      imageUrl = methodGif
      break
    default:
      break
  }
  return imageUrl ? `background-image: url(${imageUrl});padding-left: 18px;background-repeat: no-repeat;background-position: 0 0;` : ""
}

watch(
    // () => route.query.id,
    // (id) => {
    //   console.log("id", id)
    //
    //   if (!id) return
    //   useCoverageReportApi().getReportById({id: id}).then((res) => {
    //         state.reportDetail = res.data
    //         state.breadcrumbs = []
    //         getCoverageDetail({
    //           name: res.data?.name,
    //           el_type: "report",
    //           report_id: id,
    //         })
    //       }
    //   )
    // },
    {deep: true}
)

// 页面加载时
onMounted(() => {

});


</script>

<style lang="scss" scoped>

//.coverage-report {
//  position: fixed;
//  width: 100%;
//}

//.coverage-table, .coverage-code-view {
//  margin-top: 75px;
//}

@mixin default-report {
  padding-left: 18px;
  background-position: left center;
  background-repeat: no-repeat;
}

:deep(.el-progress-bar__outer) {
  background-color: #f56c6c;
}

:deep(.el-breadcrumb) {
  font-size: 14px;
  height: 16px;
  line-height: 16px;
}
</style>
