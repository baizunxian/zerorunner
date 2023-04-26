<template>
  <el-form inline ref="request-form" label-width="50px" size="small" label-position="right">
    <div class="block-title">
      <el-button size="small" type="primary" link @click="addHeaders" title="添加header">
        <el-icon><ele-CirclePlusFilled></ele-CirclePlusFilled></el-icon>add
      </el-button>
      <el-button type="primary" link @click="bulkEdit" title="文本编辑">
        {{ showBulk ? "KeyValueEdit" : "BulkEdit" }}
      </el-button>
    </div>

    <div v-show="showBulk">
      <el-input size="small" type="textarea" rows="5" v-model="headersBulk" placeholder="" show-word-limit></el-input>
    </div>

    <div v-show="!showBulk">
      <el-table
          ref="multipleTable"
          :data="headersData"
          tooltip-effect="dark"
          border
          style="width: 100%"
      >
        <el-table-column header-align='center'>
          <template #header>
            <strong style="font-size: 14px;">参数名</strong>
          </template>
          <template #default="scope">
            <el-input size="small" v-model="scope.row.key"></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="value" header-align='center'>
          <template #header>
            <strong style="font-size: 14px;">参数值</strong>
          </template>
          <template #default="scope">
            <el-input size="small" v-model.trim="scope.row.value"></el-input>
          </template>
        </el-table-column>
        <el-table-column align="center" width="50" class-name="small-padding fixed-width">
          <template #default="scope">

            <el-button size="small" type="primary" link @click="deleteHeaders(scope.$index)">
              <el-icon>
                <ele-Delete/>
              </el-icon>
            </el-button>

          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-form>
</template>

<script lang="ts">
import {defineComponent, reactive, ref, toRefs} from "vue";

export default defineComponent({
  name: 'requestHeaders',
  components: {},
  setup() {
    const formRef = ref()
    const state = reactive({
      showBulk: false,  // 启动 bulk
      headersBulk: '',  // bulk内容
      // headers
      headersData: [],  // 请求头数据

    });
    // 初始化数据
    const initForm = (formData: any) => {
      for (let key in formData.headers) {
        let head = {}
        head.key = key
        head.value = formData.headers[key]
        state.headersData.push(head)
      }
    }

    // 获取表单数据
    const getFormData = () => {
      let headers = {}
      if (state.showBulk) {
        bulkToKeyValue()
      }
      if (state.headersData.length > 0) {
        state.headersData.forEach(data => {
          if (data.key != '') {
            headers[data.key] = data.value
          }
        })
      }
      return headers
    }

    // bulk 转换
    const bulkEdit = () => {
      if (state.showBulk) {
        bulkToKeyValue()
        state.showBulk = false
      } else {
        keyValueToBulk()
        state.showBulk = true
      }
    }

    const bulkToKeyValue = () => {
      if (state.headersBulk.length > 0) {
        let snsArr = state.headersBulk.split(/[(\r\n)\r\n]+/)
        if (snsArr.length > 0) {
          let headerList = []
          snsArr.forEach(data => {
            let keyValue = data.split(':')
            let head = {}
            if (keyValue.length >= 2) {
              head.key = keyValue[0]
              head.value = keyValue[1]
            } else if (keyValue.length < 2) {
              head.key = keyValue[0]
              head.value = ''
            }
            headerList.push(head)
          })
          state.headersData = headerList
        }
      }
    }

    const keyValueToBulk = () => {
      if (state.headersData.length > 0) {
        let bulk = ''
        state.headersData.forEach(data => {
          if (data.key != '') {
            bulk = bulk + data.key + ':' + data.value + '\r\n'
          }
        })
        state.headersBulk = bulk
      }
    }

    // Headers
    const addHeaders = () => {
      state.headersData.push({key: '', value: ''})
    }
    const deleteHeaders = (index: number) => {
      state.headersData.splice(index, 1)
    }

    return {
      formRef,
      initForm,
      getFormData,
      addHeaders,
      deleteHeaders,
      bulkEdit,
      bulkToKeyValue,
      ...toRefs(state),
    };
  },
})

</script>

<style lang="scss" scoped>
.employee_body {
  margin: 10px 20px 0;
  overflow: hidden;
}

.inputclass {
  width: 300px;
}

.el-dialog {
  height: 50%;
}

table {
  width: 50%;
  border-collapse: collapse;

  tr, td {
    border: 1px solid #d2d2d6;
    padding: 5px;
  }
}

.radio-group {
  margin-bottom: 15px;
}

.title-wrap {
  font-size: 14px;
  color: #8b60f0;
  font-weight: 700;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  margin-top: 12px;

  .title {
    padding: 0 16px;
  }

  .line {
    width: 100px;
    height: 2px;
    border-bottom: 2px dashed #e1e1f5;
  }

  .add-line {
    width: 800px;
    overflow: hidden;
  }
}

.filter-item {
  color: #fff;
  background-color: #5bc0de;
  border-color: #ffffff;
  margin-bottom: 10px;

  &:hover {
    color: #fff;
    background-color: #31b0d5;
    border-color: #ffffff;
  }
}
</style>

<style lang="scss" scoped>
/* jsoneditor右上角默认有一个链接,加css去掉了 */
.jsoneditor-poweredBy {
  display: none;
}

.ace_gutter {
  background: #FFF
}

.jsoneditor-vue .jsoneditor {
  border: 0;

  .jsoneditor-menu {
    // background: #ebebeb;
    background-color: #ebebeb;
    border-bottom: 0;

    .jsoneditor-modes {
      color: #000;
    }

    .jsoneditor-outer {
      background: #ebebeb;
    }

    button {
      outline: none;
      background-color: #5bc0de;

      &:hover {
        background-color: #5bc0de;
      }
    }
  }
}

/* el-input */
:deep(.el-input__inner) {
  font-weight: bold;
}

.block-title {
  position: relative;
  padding-left: 11px;
  font-size: 14px;
  font-weight: 600;
  height: 28px;
  line-height: 28px;
  background: #f7f7fc;
  color: #333333;
}
</style>