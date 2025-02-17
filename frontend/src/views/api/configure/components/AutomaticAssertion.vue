<template>
  <div>
    <el-collapse Vlaue="1">
      <template>
        <el-collapse-item :name="index" v-for="(record, index) in details[0].records"
                          :key="guid2() + index + 'records1' ">
          <div slot="title" style="width: 100%; padding: 5px 0;">
            <div>
              <div>
                <div v-if="record.status === 'success'" style="font-size: 16px; padding: 3px 0;">
                  {{ record.name }}
                  <el-tag type="success">pass</el-tag>
                </div>
                <div v-if="record.status === 'failure'" style="font-size: 16px; padding: 3px 0;">
                  {{ record.name }}
                  <el-tag type="danger">fail</el-tag>
                </div>
                <div v-if="record.status === 'error'" style="font-size: 16px; padding: 3px 0;">
                  {{ record.name }}
                  <el-tag type="danger">error</el-tag>
                </div>
                <div v-if="record.status === 'skipped'" style="font-size: 16px; padding: 3px 0;">
                  {{ record.name }}
                  <el-tag type="info">skip</el-tag>
                </div>
              </div>
              <div class="node-header">
                <div class="node-header-left">
                  <span class='node-time'>{{ record.start_timestamp }}</span>
                  <span class='node-duration'>response_time: {{record.meta_data.response.response_time_ms}} ms</span>
                </div>
              </div>
            </div>
          </div>
          <div class='collapsible-body'>

            <div class='node-steps'>
              <table class='bordered table-results' style="width: 100%;">
                <thead>
                <tr>
                  <th>状态</th>
                  <th>参数</th>
                  <th>详情</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td></td>
                  <td><strong style="color: coral;">Request</strong></td>
                  <td></td>
                </tr>

                <tr class='info' status='info'>
                  <td class='status info' title='info' alt='info' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>url</td>
                  <td class='step-details'>{{ record.meta_data.request.url }}</td>
                </tr>

                <tr class='info' status='info'>
                  <td class='status info' title='info' alt='info' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>method</td>
                  <td class='step-details'>{{ record.meta_data.request.method }}</td>
                </tr>

                <tr class='info' status='info'>
                  <td class='status info' title='info' alt='info' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>status_code</td>
                  <td class='step-details'>{{ record.meta_data.response.status_code }}</td>
                </tr>
                <template v-for="(value, key, index) in record.meta_data.request">
                  <tr v-if="key!=='url' && key !== 'method' && key !== 'start_timestamp'"
                      :key="guid2() + index + 'request'">
                    <td class='status debug' title='debug' alt='debug' align="center"><i
                        class='el-icon-pie-chart'></i></td>
                    <td class='timestamp'>{{ key }}</td>
                    <td class='step-details' v-if="key === 'headers'">
                      <div v-for="(header_value, header_key) in record.meta_data.request.headers"
                           :key="guid2() + header_key + 'headers'">
                        <strong>{{ header_key }}</strong>: {{ header_value }}
                      </div>
                    </td>
                    <td class='step-details' v-else-if="key === 'json'">
                      <json-viewer
                          :value="record.meta_data.request.json"
                          :expand-depth="5"
                          :copyable="copyable"
                          :boxed="true"
                          sort
                      />
                    </td>
                    <td v-else>{{ value }}</td>
                  </tr>
                </template>
                <tr>
                  <td></td>
                  <td><strong style="color: coral;">Response</strong></td>
                  <td></td>
                </tr>
                <template v-for="(value, key, index) in record.meta_data.response">
                  <tr v-if="key!=='content' &&
                      key !== 'start_timestamp' &&
                      key !== 'response_time_ms' &&
                      key !== 'content_size' &&
                      key !== 'content_type' &&
                      key !== 'status_code' &&
                      key !== 'reason' &&
                      key !== 'ok' &&
                      key !== 'encoding' &&
                      key !== 'url'"
                      :key="guid2() + index+'response'">
                    <td class='status debug' title='debug' alt='debug' align="center"><i
                        class='el-icon-pie-chart'></i></td>
                    <td class='timestamp'>{{ key }}</td>
                    <td class='step-details' v-if="key === 'headers'">
                      <div v-for="(header_value, header_key) in record.meta_data.response.headers"
                           :key="guid2() + header_key + 'headers'">
                        <strong>{{ header_key }}</strong>: {{ header_value }}
                      </div>
                    </td>
                    <td class='step-details'
                        v-else-if="key === 'json' && record.meta_data.response.json!=null">
                      <img v-if="record.meta_data.response.content_type === 'image'"
                           :src="record.meta_data.response.content" alt="">
                      <json-viewer
                          :value="record.meta_data.response.json"
                          :expand-depth="5"
                          :copyable="copyable"
                          boxed
                          sort
                      />
                    </td>
                    <td class='step-details' v-else-if="key === 'text'">
                      <img v-if="record.meta_data.response.content_type === 'image'"
                           :src="record.meta_data.response.content" alt="">
                      <json-viewer
                          v-else
                          :value="record.meta_data.response.text"
                          :expand-depth="1"
                          :copyable="copyable"
                          boxed
                          sort
                      />
                    </td>
                    <td v-else>{{ value }}</td>
                  </tr>
                </template>

                <tr class='log' status='pass'>
                  <td class='status pass' title='pass' alt='pass' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>Validators</td>
                  <td class='timestamp' v-if="record.meta_data.validators.length < 1">无校验</td>
                  <td class='step-details' v-else>
                    <div v-for="validator in record.meta_data.validators"
                         :key="guid2() + validator.check_result + 'validators'">
                      <el-tag :type="validator.check_result === 'pass'? 'success':'danger'"
                              effect="dark">
                        {{ validator.check_result }}
                      </el-tag>
                      <strong> {{ validator.check }} {{ validator.comparator }}:</strong>
                      {{ [validator.expect, validator.check_value] }}
                    </div>
                  </td>
                </tr>
                <tr class='info' status='info'>
                  <td class='status info' title='info' alt='info' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>Statistics</td>
                  <td class='step-details'>
                    <div>请求内容大小(bytes): {{ record.meta_data.response.content_size }}</div>
                    <div>响应时间(ms): {{ record.meta_data.response.response_time_ms }}</div>
                    <div>用时(ms): {{ record.meta_data.response.elapsed_ms }}</div>
                  </td>
                </tr>
                <tr v-if="record.attachment.length > 0" class='log' status='fail'>
                  <td class='status fail' title='fail' alt='fail' align="center"><i
                      class='el-icon-pie-chart'></i></td>
                  <td class='timestamp'>exception:</td>
                  <td class='step-details'>
                    <pre>{{ record.attachment }}</pre>
                  </td>
                </tr>


                </tbody>
              </table>
            </div>
          </div>
        </el-collapse-item>
      </template>
    </el-collapse>
    <json-viewer
        :value="json_result"
        :expand-depth="5"
        :copyable="copyable"
        :boxed="true"
        sort
    />

    <el-form :inline="true" v-model="assertForm" style="padding-top: 10px">

      <el-form-item label="提取字段">
        <el-input v-model="assertForm.field" placeholder="提取字段" style="width: 100px;">提取字段</el-input>
      </el-form-item>

      <el-form-item label="提取字段值">
        <el-input v-model="assertForm.field_value" placeholder="提取字段值" style="width: 100px;">提取字段值</el-input>
      </el-form-item>

      <el-form-item label="提取层级">
        <el-input v-model.number="assertForm.level_num" placeholder="输入提取层级" style="width: 100px;">提取层级</el-input>
      </el-form-item>

      <el-form-item>
        <el-button size="mini" type="primary" @click="getCaseAssertion" style="margin: 5px">断言生成</el-button>
        <el-button size="mini" type="success" @click="setValidate" style="margin: 5px">设置断言</el-button>
      </el-form-item>
    </el-form>

    <el-table
        :header-cell-style="tabelheadercolor"
        ref="multipleTable"
        :data="validate_list"
        border
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleValidateSelectionChange"
    >
      <el-table-column
          type="selection"
          width="55">
      </el-table-column>

      <el-table-column prop="key" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">校验参数</strong>
        </template>
        <template #default="{row}">
          <el-input v-model="row.check"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="Comparator" width="120" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">对比规则</strong>
        </template>
        <template #default="{row}">
          <el-select v-model="row.comparator" placeholder="请选择">
            <el-option
                v-for="item in comparatorOptions"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
          </el-select>
        </template>
      </el-table-column>

      <el-table-column prop="type" width="120" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">类型</strong>
        </template>
        <template #default="{row}">
          <el-select v-model="row.type" placeholder="请选择">
            <el-option
                v-for="item in typeOptions"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
          </el-select>
        </template>
      </el-table-column>

      <el-table-column prop="Expected" label="Expected" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">校验值</strong>
        </template>
        <template #default="{row}">
          <el-input v-model="row.expected"></el-input>
        </template>
      </el-table-column>
    </el-table>


    <el-form :inline="true" v-model="extractForm" style="padding-top: 10px">

      <el-form-item label="提取字段">
        <el-input v-model="extractForm.field" placeholder="提取字段" style="width: 100px;">提取字段</el-input>
      </el-form-item>

      <el-form-item>
        <el-button size="mini" type="primary" @click="getCaseExtract" style="margin: 5px">提取生成</el-button>
        <el-button size="mini" type="success" @click="setExtract" style="margin: 5px">设置提取</el-button>
      </el-form-item>
    </el-form>

    <el-table
        :header-cell-style="tabelheadercolor"
        ref="multipleTable"
        :data="extract_list"
        border
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleExtractSelectionChange"
    >

      <el-table-column
          type="selection"
          width="55">
      </el-table-column>
      <el-table-column header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">变量名</strong>
        </template>
        <template #default="{row}">
          <el-input v-model="row.key"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="value" header-align='center'>
        <template #header>
          <strong style="font-size: 14px;">提取值</strong>
        </template>
        <template #default="{row}">
          <el-input v-model="row.value"></el-input>
        </template>
      </el-table-column>

    </el-table>

  </div>
</template>

<script>
// import JsonViewer from '@/utils/vue-json-viewer'
// import 'vue-json-viewer/style.css'
// import {get_case_assertion} from '@/api/apiInfo'

export default {
  components: {
    JsonViewer
  },
  name: 'AutomaticAssertion',
  props: {
    reportData: Object
  },

  data() {
    return {
      tabelheadercolor: {color: '#000', background: '#f5f5f5'},
      copyable: {copyText: '复制', copiedText: '复制成功'},
      details: this.reportData.result.details,
      json_result: this.reportData.json_result,
      typeOptions: ['string', 'int', 'float', 'boolean', 'dict', 'list'],
      comparatorOptions: [
        'equals',
        'contains',
        'startswith',
        'endswith',
        'regex_match',
        'type_match',
        'contained_by',
        'less_than',
        'less_than_or_equals',
        'greater_than',
        'greater_than_or_equals',
        'not_equal',
        'string_equals',
        'length_equals',
        'length_greater_than',
        'length_greater_than_or_equals',
        'length_less_than',
        'length_less_than_or_equals',
        'json_equals',
      ],
      validate_list: [],
      extract_list: [],
      select_validate_list: [],
      select_extract_list: [],
      assertForm: {
        level_num: 1,
        field: '',
        field_value: '',
      },
      extractForm: {
        level_num: 1,
        field: '',
      }
    }
  },
  methods: {

    getCaseAssertion() {
      this.assertForm.data = this.json_result
      get_case_assertion(this.assertForm)
          .then(res => {
            this.validate_list = res.data.validate_list
          })
    },
    getCaseExtract() {
      this.extractForm.data = this.json_result
      get_case_assertion(this.extractForm)
          .then(res => {
            this.extract_list = res.data.extract_list
          })
    },

    resetDate() {
      this.validate_list = []
    },
    handleValidateSelectionChange(row) {
      this.select_validate_list = row
    },
    handleExtractSelectionChange(row) {
      this.select_extract_list = row
    },
    setValidate() {
      if (this.select_validate_list.length > 0) {
        this.$emit('setValidate', this.select_validate_list)
        this.$message.success('设置成功！')
      } else {
        this.$message.warning('请选勾选需要设置的断言！')
      }
    },

    setExtract() {
      if (this.select_extract_list.length > 0) {
        this.$emit('setExtract', this.select_extract_list)
        this.$message.success('设置成功！')
      } else {
        this.$message.warning('请选勾选需要设置的提取！')
      }
    },

    guid2() {
      function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
      }

      return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4())
    },
  }
}
</script>

<style lang="scss" scoped>

.container {
  background: #fff;
}

.header {
  color: #111;
  background-color: #f5f5f5 !important;
  display: flex;
  justify-content: space-between;

  .header-left {
    line-height: 55px;
    display: flex;
  }
}

.el-main {
  padding: 0;
  // background:#fff ;
}

.main {
  .main-start {
    .subview-right {
      width: 100%;
      height: 615px;
      border-right: 1px solid #eee;
    }

    .subview-left {
      resize: horizontal;
      height: 615px;
      width: 276px;
      border-right: 1px solid #eee;
      border-left: 1px solid #eee;
      max-width: 80%;
      min-width: 10%;
      resize: horizontal;
      width: 27%;
      display: block;
      overflow-y: auto;
      padding: 0 20px;

      .view-summary {
        height: 300px;
      }

      ul {
        padding: 0;

        li {
          list-style-type: none;
          border-bottom: 1px solid #eee;
          margin: 0 -20px;
          padding: 10px 20px;

          &:active {
            // background: #f7f7f7;
            font-weight: 600;
          }

          &:first-child {
            border-top: 1px solid #eee;
          }

          .test-heading {
            .test-name {
              font-size: 16px;
              // width: 100% !important;
              display: inline-block;
              word-break: break-all;
            }

            .test-time {
              font-size: 12px;
              font-weight: 400;
            }

            .test-status {
              text-transform: capitalize;
              font-size: 13px;
              float: right
            }

            .pass {
              color: #32cd32;
            }

            .fail {
              color: red;
            }
          }

        }

        li.active {
          background: #f7f7f7;
          font-weight: 600;
        }
      }
    }

    .main-start-tag {
      height: 40px;
      padding: 10px 10px;

      .tag {
        margin-left: 10px;
      }
    }

    .test-polar {
      padding: 10px;
      border: 1px solid #ddd;
    }
  }
}

.start-time {
  background: #00c853;
  color: #fff;
}

.label {
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 90%;
  font-weight: 600;
}

.end-time, .category-status > .fail {
  background: #ef5350;
  color: #fff;
}

.test-desc {
  padding-top: 7px;
  font-size: 14px;
}

.hide {
  display: none;
}

.tip {
  padding: 4px 4px;
  font-size: 70%;
  color: #111;

  p {
    margin: 0;
  }
}

.node-header {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

:deep(.el-collapse-item__header) {
  line-height: normal;
  // border: 1px solid #EBEEF5;
  height: 60px;
  border-top: 1px solid #EBEEF5;
  border-left: 1px solid #EBEEF5;
  border-right: 1px solid #EBEEF5;
  padding: 8px;
}

:deep(.el-collapse-item__wrap) {
  line-height: normal;
  border-left: 1px solid #EBEEF5;
  border-right: 1px solid #EBEEF5;
}

:deep(.el-collapse-item) {
  margin-top: 10px;
  margin-bottom: 10px;
}

:deep(.el-collapse) {
  // margin-top: 10px;
  border: none;
}

:deep(.jv-code) {
  overflow: auto;
}
</style>