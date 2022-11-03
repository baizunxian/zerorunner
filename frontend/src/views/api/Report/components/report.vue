<template>
  <div class="">
<!--    <el-card shadow="hover" style="height: 100%;">-->

      <el-row>
        <el-col :span="12" style="padding-left: 5px; padding-right: 5px; width: 100%">
          <div style="border: 1px solid rgb(220, 218, 226); padding: 10px; border-radius: 4px; width: 100%">
            <div class="suites_chart" ref="suitesChartRef" style="width: 100%; height: 120px;"></div>
          </div>
        </el-col>
        <el-col :span="12" style="padding-left: 5px; padding-right: 5px; width: 100%">
          <div style="border: 1px solid rgb(220, 218, 226); padding: 10px; border-radius: 4px; width: 100%">
            <div ref="stepChartRef" style="width: 100%; height: 120px;"></div>
            <!--            <div class="tip">-->
            <!--              <p>{{ reportTestCaseData.testcase.stat.teststeps.successes }} 用例通过</p>-->
            <!--              <p>{{ reportTestCaseData.testcase.stat.teststeps.failures }} 用例失败</p>-->
            <!--            </div>-->
          </div>
        </el-col>
      </el-row>

      <el-row style="padding-top: 5px">
        <!-- 测试用例 -->
        <el-col :span="6" style="padding-left: 5px; padding-right: 5px;">

          <div style="border: 1px solid rgb(220, 218, 226); padding: 10px; border-radius: 4px;">

            <div style="position: relative;">
              <!--            <h3 class="block-title">报告详情</h3>-->
              <el-tag type="success" style="margin-right: 10px; background-color: #e7faf0; color: #13ce66;">
                total:{{ reportTestCaseData.testcase.stat.teststeps.total }}
              </el-tag>
              <el-tag type="success" style="margin-right: 10px; background-color: #e7faf0; color: #13ce66;">
                Pass:{{ reportTestCaseData.testcase.stat.teststeps.successes }}
              </el-tag>
              <el-tag type="warning" style="margin-right: 10px;">
                Fail:{{ reportTestCaseData.testcase.stat.teststeps.failures }}
              </el-tag>
              <!--            <el-tag type="danger" style="margin-right: 10px;">-->
              <!--              Error: {{ reportBody.stat.teststeps.errors }}-->
              <!--            </el-tag>-->
            </div>

            <div class="sys-list box-height">
              <el-tree
                  :data="reportTestCaseData.testcase.details"
                  node-key="id"
                  :props="{children: 'step_datas', label:'name' }"
                  ref="tree"
                  @node-click="reportNodeClick"
                  :highlight-current='true'
              >
                <template #default="scope">
                  <div class="custom-node">
                    <span>
                      <el-icon v-if="!scope.data.step_datas && scope.data.success"
                               style="color: #67c23a;  vertical-align:bottom; height: 100%; display: inline-block;">
                        <ele-CircleCheckFilled></ele-CircleCheckFilled>

                      </el-icon>
                      <el-icon v-if="!scope.data.step_datas && !scope.data.success"
                               style="color: #ee6666;  vertical-align:bottom; height: 100%; display: inline-block;">
                        <ele-CircleCloseFilled></ele-CircleCloseFilled>
                      </el-icon>
                      <span v-if="!scope.data.step_datas" style="padding-left: 5px">{{ scope.data.name }}</span>
                      <span v-else style="padding-left: 5px; font-weight: bold">{{ scope.data.name }}</span>
                    </span>
                  </div>
                </template>
              </el-tree>
            </div>
          </div>
        </el-col>

        <el-col v-show="nodeStepData.name" :span="18" style="padding-left: 5px; padding-right: 5px;">
          <div style="border: 1px solid rgb(220, 218, 226); padding: 10px; border-radius: 4px;">
            <div class="box-height">

              <!--      step title        -->
              <div class="step">
                <div>
                  <h2 class="step__header">
                    <div class="step__header__tab">
                      <el-tag class="ml-2" :type="nodeStepData.success? 'success': 'danger'" effect="dark">
                        {{ nodeStepData.success ? '通过' : '不通过' }}
                      </el-tag>
                    </div>
                    <div class="step__header__name">
                      <span>{{ reportTestCaseData.step.name }}</span>
                    </div>
                  </h2>
                </div>
                <div style="padding-bottom: 5px">
                  <el-tag type="success" effect="dark">执行用时 {{ reportTestCaseData.step.stat.elapsed_ms }}</el-tag>
                  <el-tag type="success" effect="dark" style="margin-left: 5px">响应时间
                    {{ reportTestCaseData.step.stat.response_time_ms }}
                  </el-tag>
                </div>
              </div>

              <!--   request       -->
              <div class="request">
                <div class="request__header">
                  <h3 class="request__header__name title">请求[request]</h3>
                </div>
                <div class="request__body">
                  <table class="table">
                    <tbody>
                    <!--                <tr>-->
                    <!--                  <th>222</th>-->
                    <!--                  <th>33</th>-->
                    <!--                </tr>-->
                    <tr>
                      <td class="table__parameter">url</td>
                      <td class="table__content">
                        {{ reportTestCaseData.step.request.url }}
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">method</td>
                      <td class="table__content">
                        {{ reportTestCaseData.step.request.method }}
                      </td>
                    </tr>
                    <tr>
                      <td class="table__parameter">status_code</td>
                      <td class="table__content">
                        {{ reportTestCaseData.step.response.status_code }}
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">headers</td>
                      <td class="table__content">
                        <div v-for="(header_value, header_key) in reportTestCaseData.step.request.headers"
                             :key="guid2() + header_key + 'headers'">
                          <strong>{{ header_key }}</strong>: {{ header_value }}
                        </div>
                        <!--                    {{ reportTestCaseData.step.request.headers }}-->
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">json</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.request.json"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">body</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.request.body"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>


                    </tbody>
                  </table>
                </div>
              </div>

              <!--            response-->
              <div class="response">
                <div class="response__header">
                  <h3 class="response__header__name title">响应[Response]</h3>
                </div>
                <div class="response__body">
                  <table>
                    <tbody>

                    <tr>
                      <td class="table__parameter">headers</td>
                      <td class="table__content">
                        <div v-for="(header_value, header_key) in reportTestCaseData.step.response.headers"
                             :key="guid2() + header_key + 'headers'">
                          <strong>{{ header_key }}</strong>: {{ header_value }}
                        </div>
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">cookies</td>
                      <td class="table__content">
                        {{ reportTestCaseData.step.request.cookies }}
                      </td>
                    </tr>
                    <tr>
                      <td class="table__parameter">text</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.response.text"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">json</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.response.json"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">body</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.response.body"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>

              </div>

              <!--            用例校验-->
              <div class="case_info">
                <div class="case_info__header">
                  <h3 class="case_info__header__name title">详细信息[case_info]</h3>
                </div>
                <div class="case_info__body">
                  <table>
                    <tbody>

                    <tr>
                      <td class="table__parameter">错误[error_massage]</td>
                      <td class="table__content">
                        <pre>{{ reportTestCaseData.step.message }}</pre>
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">校验[validators]</td>
                      <td class='timestamp' v-if="!reportTestCaseData.step.validators.validate_extractor">无校验</td>
                      <td class='step-details' v-else>
                        <div style="padding: 1px 0"
                             v-for="validator in reportTestCaseData.step.validators.validate_extractor"
                             :key="guid2() + validator.check_result">
                          <el-tag :type="validator.check_result === 'pass'? 'success':'danger'" effect="dark">
                            {{ validator.check_result }}
                          </el-tag>
                          <strong> {{ validator.check }} {{ validator.comparator }}:</strong>
                          {{ [validator.expect, validator.check_value] }}
                        </div>
                      </td>
                    </tr>

                    <tr>
                      <td class="table__parameter">变量[variables]</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.variables"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>
                    <tr>
                      <td class="table__parameter">输出变量[export_vars]</td>
                      <td class="table__content">
                        <json-viewer
                            :value="reportTestCaseData.step.export_vars"
                            :expand-depth="5"
                            copyable
                            :boxed="true"
                            sort
                        />
                      </td>
                    </tr>
                    <!--                <tr>-->
                    <!--                  <td>Statistics</td>-->
                    <!--                  <td>-->
                    <!--                    {{ reportTestCaseData.step.Statistics}}-->
                    <!--                  </td>-->
                    <!--                </tr>-->


                    </tbody>
                  </table>
                </div>

                <!--            {{ reportTestCaseData }}-->
              </div>
            </div>
          </div>
        </el-col>

      </el-row>
<!--    </el-card>-->
  </div>
</template>

<script lang="ts">
import "vue3-json-viewer/dist/index.css"
import {JsonViewer} from 'vue3-json-viewer'
import * as ECharts from 'echarts'
import {defineComponent, nextTick, onMounted, reactive, ref, toRefs} from "vue";


export default defineComponent({
  name: 'testReport',
  components: {
    JsonViewer,
  },
  props: {
    reportBody: {
      type: Object,
      required: true
    }
  },

  created() {
    if (this.$props.reportBody) {
      this.initReportData()
    }
  },

  setup(props) {
    const suitesChartRef = ref()
    const stepChartRef = ref()
    const state = reactive({
      suites_index: 0,
      reportData: {},
      nodeStepData: {},  // 选中的用例步骤数据
      reportTestCaseData: {
        testcase: {
          success: '',
          stat: {},
          time: {},
          platform: {},
          details: {},
        },
        step: {
          success: '',
          name: '',
          case_id: '',
          message: '',
          variables: {},
          request: {},
          response: {},
          stat: {},
          address: {},
          validators: {},
          export_vars: {},
        }
      },
      test_suite_success: 0,
      test_suite_fail: 0,
      // uuid: guid2(),
      copyable: {copyText: '复制', copiedText: '复制成功'},
      test_data: {}
    });

    // 初始化报告数据
    const initReportData = () => {
      // state.detailData = state.test_data.data.details
      // 用例 成功状态
      let test_data: any = props.reportBody
      // let test_data = state.test_data.data
      state.nodeStepData = {} // 选中数据
      state.reportTestCaseData.testcase.success = test_data.success
      state.reportTestCaseData.testcase.stat = test_data.stat
      state.reportTestCaseData.testcase.time = test_data.time
      state.reportTestCaseData.testcase.platform = test_data.platform
      state.reportTestCaseData.testcase.details = test_data.details

      // 步骤详情
      if (state.nodeStepData.length > 0) {
        state.reportTestCaseData.step.success = state.nodeStepData.success
      }
    }

    // 节点点击赋值
    const reportNodeClick = (node: any) => {
      if (!node.step_datas) {
        state.nodeStepData = node
        state.reportTestCaseData.step.success = node.success
        state.reportTestCaseData.step.name = node.name
        state.reportTestCaseData.step.case_id = node.case_id
        state.reportTestCaseData.step.message = node.message
        state.reportTestCaseData.step.variables = node.variables
        state.reportTestCaseData.step.export_vars = node.export_vars
        state.reportTestCaseData.step.stat = node.data.stat
        state.reportTestCaseData.step.address = node.data.address
        state.reportTestCaseData.step.validators = node.data.validators
        if (node.data.req_resps.length > 0) {
          let req_resps_data = node.data.req_resps[0]
          state.reportTestCaseData.step.request = req_resps_data.request
          state.reportTestCaseData.step.response = req_resps_data.response
        } else {
          state.reportTestCaseData.step.request = {}
          state.reportTestCaseData.step.response = {}
        }

      }
    }


    // 用例图
    const initStepData = () => {
      let stepECharts = ECharts.init(stepChartRef.value)
      stepECharts.setOption({
        title: {
          text: '用例结果',
          subtext: `${state.reportTestCaseData.testcase.stat.teststeps.successes} 用例通过
          \n${state.reportTestCaseData.testcase.stat.teststeps.failures} 用例失败`,
          x: 'left',
          textStyle: {
            color: '#000000',
            fontSize: '16',
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          top: '0%',
          left: 'right',
          data: ['成功', '失败']
        },
        series: [
          {
            name: '用例结果',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              {
                name: '成功',
                itemStyle: {color: '#91cc75'},
                value: state.reportTestCaseData.testcase.stat.teststeps.successes,
              },
              {
                name: '失败',
                itemStyle: {color: '#ee6666'},
                value: state.reportTestCaseData.testcase.stat.teststeps.failures,
              },
            ]
          }
        ]
      })
      // let option =
    }
    // 套件图
    const initSuitesData = () => {
      let suiteECharts = ECharts.init(suitesChartRef.value)
      suiteECharts.setOption({
        title: {
          text: '套件结果',
          subtext: `${state.reportTestCaseData.testcase.stat.testcases.success} 套件通过
          \n${state.reportTestCaseData.testcase.stat.testcases.fail} 套件失败`,
          x: 'left',
          textStyle: {
            color: '#000000'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          top: '0%',
          left: 'right',
          data: ['成功', '失败']
        },
        series: [
          {
            name: '套件结果',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              {
                value: state.reportTestCaseData.testcase.stat.testcases.success,
                name: '成功',
                itemStyle: {color: '#91cc75'}
              },
              {
                value: state.reportTestCaseData.testcase.stat.testcases.fail,
                name: '失败',
                itemStyle: {color: '#ee6666'}
              },
            ]
          }
        ]
      })
    }

    const guid2 = () => {
      function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
      }

      return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4())
    }

    onMounted(() => {
      if (props.reportBody) {
        initSuitesData()
        initStepData()
        // 窗口变动自适应大小
        window.onresize = () => {
          ECharts.init(stepChartRef.value).resize();
          ECharts.init(suitesChartRef.value).resize();
        }
        // 加载完dom重新渲染
        nextTick(() => {
          ECharts.init(stepChartRef.value).resize();
          ECharts.init(suitesChartRef.value).resize();
        })
      }
    })

    return {
      suitesChartRef,
      stepChartRef,
      initSuitesData,
      initStepData,
      initReportData,
      reportNodeClick,
      // initTestCount,
      guid2,
      ...toRefs(state),
    };
  }
})

</script>

<style lang="scss" scoped>

.test_report {
  height: calc(100vh - 100px);
}

th, td {
  border-bottom: 1px solid #d9d9d9 !important;
}

th {
  padding: 5px 10px;
}

td {
  padding: 7px 10px;
  word-break: break-all;
}


.box-height {
  overflow-y: auto;
  //height: 100%;
  height: calc(100vh - 30px - 34px - 49px - 100px);
}

.step {
  border-bottom: 1px solid #eceff1;

  .step__header {
    padding: 0 0 10px;
    width: 100%;
    display: flex;
    position: relative;
    margin: 7px 0 0;
    font-size: 20px;
    font-weight: 700;

    .step__header__name {
      padding-left: 10px;
    }

    .step__header__tab {

    }
  }
}


// 请求
.title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 28px;
  line-height: 28px;
  background: #f7f7fc;
  color: #333333;
}

.title::before {
  content: '';
  position: absolute;
  top: 7px;
  left: 0;
  width: 3px;
  height: 14px;
  background: #409eff;
}

table {
  width: 100%;
}

.table {
  width: 100%;
}

.table__parameter {
  width: 20%;
}

.table__content {
  width: 80%;
}

:deep(.el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content) {
  background-color: #fffacd;
}

pre, .code-block {
  background-color: #f8f9fa;
  border: 1px solid #ebedef;
  border-radius: 4px;
  color: #222 !important;
  font-family: Consolas, monospace;
  font-size: 13px;
  margin: 0;
  padding: 7px 10px;
  white-space: pre-wrap;
}

.pre {
  border: none;
  white-space: pre;
  padding: 5px 0 5px 30px;
  font-family: Consolas;
  font-size: 13px;
}

.pre > pre {
  background: transparent;
  border: none;
}

.dark pre, .dark #test-view-charts .card-panel, .dark .scenario, .dark .background, .dark ul.steps, .dark .collapsible > li, .dark #charts-row .card-panel {
  border: 1px solid #333 !important;
}
</style>