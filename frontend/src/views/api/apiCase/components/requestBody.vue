<template>
  <el-form inline ref="request-form" label-width="50px" size="small" label-position="right">
    <!-- data -->
    <div style="border-bottom: 1px solid #E6E6E6; display: flex; justify-content: space-between">
      <div>
        <el-radio-group
            size="small"
            v-model="mode"
            class="radio-group"
            @change="radioChange"
        >
          <!--      <el-radio label="data">data</el-radio>-->
          <el-radio label="form_data">form-data</el-radio>
          <el-radio label="raw">raw</el-radio>

          <el-popover
              v-if="mode === 'raw'"
              :hide-after="0"
              placement="bottom"
              trigger="click"
              popper-class="popover-class"
              ref="rawPopoverRef">
            <template #reference>
              <el-button size="small" type="primary" link @click="showPopover">
                {{ language }}
                <el-icon v-if="popoverOpen">
                  <ele-ArrowUp></ele-ArrowUp>
                </el-icon>
                <el-icon v-else>
                  <ele-ArrowDown></ele-ArrowDown>
                </el-icon>
              </el-button>
            </template>
            <div class="dropdown-menu">
              <div
                  v-for="language in languageList"
                  :key="language"
                  @click="handleLanguage(language)"
                  class="dropdown-menu-item">

                  <span>
                    {{ language }}
                  </span>
              </div>
            </div>

          </el-popover>
        </el-radio-group>
      </div>
    </div>

    <div v-if="mode === 'raw'" style="padding-top: 8px;">
      <div style="border: 1px solid #E6E6E6">
        <monaco-editor
            style="height: 420px"
            ref="monacoEditRef"
            v-model:value="rawData"
            v-model:long="long"
        ></monaco-editor>
      </div>
    </div>
    <!---------------------------params------------------------------------>
    <div v-if="mode === 'params'">
      <div class="block-title">
        <el-button size="small" type="primary" link @click="addParams" title="add params">
          <el-icon>
            <ele-CirclePlusFilled></ele-CirclePlusFilled>
          </el-icon>
          add
        </el-button>
      </div>
      <div>
        <el-table
            ref="paramsDataTableRef"
            :data="paramsData"
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

          <el-table-column prop="type" width="120" header-align='center'>
            <template #header>
              <strong style="font-size: 14px;">参数类型</strong>
            </template>
            <template #default="scope">
              <el-select size="small" v-model="scope.row.type" placeholder="请选择">
                <el-option
                    v-for="item in dataTypeOptions"
                    :key="item"
                    :label="item"
                    :value="item">
                </el-option>
              </el-select>
            </template>
          </el-table-column>

          <el-table-column prop="value" header-align='center'>
            <template #header>
              <strong style="font-size: 14px;">参数值</strong>
            </template>
            <template #default="scope">
              <el-input size="small" v-model="scope.row.value"></el-input>
            </template>
          </el-table-column>
          <el-table-column align="center" width="50" class-name="small-padding fixed-width">
            <template #default="scope">
              <el-button size="small" type="primary" link @click="deleteParams(scope.$index)">
                <el-icon>
                  <ele-Delete/>
                </el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <!--    form-data-->
    <div v-if="mode === 'form_data'">
      <div>
        <el-row justify="space-between"
                v-for="(data, index) in formData"
                :key="index"
                align="middle"
                class="el-row--flex"
                style="padding: 5px 0"
        >
          <!--            参数名-->
          <el-col :span="8">
            <el-input type="primary"
                      size="small"
                      maxlength="200"
                      placeholder="Key"
                      v-model="data.key">
              <template #suffix>
                {{ data.key.length }}/200
              </template>
              <template #append>
                <el-select size="small"
                           style="background-color: #ffffff; width: 60px"
                           v-model="data.type"
                           placeholder="请选择">
                  <el-option
                      v-for="item in formDatatypeOptions"
                      :key="item"
                      :label="item"
                      :value="item">
                  </el-option>
                </el-select>
              </template>

            </el-input>
          </el-col>

          <!--参数值-->
          <el-col :span="8">
            <div class="file-input-container" v-if="data.type === 'file'">
              <div class="file-input">
                <input type="file"
                       :id="'selectFile' + index"
                       @change="fileChange($event, data)"
                       class="file-input__native">
                <el-button v-if="!data.value.name"
                           type="info"
                           size="small"
                           @click="selectFile(index)">选择文件
                </el-button>

                <div v-else class="file-input__name">
                  <div class="file-input__name__title" :title="data.value.name">{{ data.value.name }}</div>
                  <el-button class="file-input__name__delete-icon" size="small" type="primary" link
                             @click="deletedFile(data, index)">
                    <el-icon>
                      <ele-Close/>
                    </el-icon>
                  </el-button>
                </div>
              </div>
            </div>
            <el-input size="small"
                      v-else
                      placeholder="Value"
                      v-model="data.value"></el-input>
          </el-col>

          <el-col :span="5">
            <el-input type="primary"
                      size="small"
                      maxlength="200"
                      placeholder="备注"
                      v-model="data.remarks">
            </el-input>
          </el-col>

          <el-col :span="1">
            <el-button type="danger" circle @click="deleteFormData(index)"
                       :disabled="formData.length === index  + 1 ">
              <el-icon>
                <ele-Delete/>
              </el-icon>
            </el-button>
          </el-col>
        </el-row>
      </div>
    </div>
  </el-form>
</template>

<script lang="ts">
import {defineComponent, reactive, ref, toRefs, watch} from "vue";
import {useFileApi} from '/@/api/useSystemApi/file'
import {ElMessage} from "element-plus";
import {handleEmpty} from "/@/utils/other";

export interface StateData {
  mode: string,
  language: string,
  languageList: Array<string>,
  popoverOpen: boolean,
  bodyData: Array<any>,
  rawData: string,
  paramsData: Array<any>,
  dataTypeOptions: Array<string>,
  formData: Array<any>,
  formDatatypeOptions: Array<string>,
  fileData: object,
  long: string,
}

export default defineComponent({
  name: 'requestBody',
  setup(props, {emit}) {
    const formDataRef = ref()
    const rawPopoverRef = ref()
    const monacoEditRef = ref()

    const state = reactive<StateData>({
      mode: 'raw',
      language: 'JSON',
      languageList: ['JSON', 'Text'],
      popoverOpen: false,
      // body
      bodyData: [],
      rawData: "",
      paramsData: [],
      dataTypeOptions: ['string', 'int', 'float', 'boolean'],
      // formData
      formData: [],
      formDatatypeOptions: ['text', 'file'],
      fileData: {},

      //monaco
      long: 'json',
    });

    // 初始化表单
    const setData = (data: any) => {
      let mode = data.mode

      if (mode === 'form_data') {
        state.formData = data.data ? data.form_data : []
      }

      if (mode === 'raw') {
        state.rawData = data.data.replace('/\\n/g', "\n")
        state.language = data.language
      }
    }

    // 获取是否填写状态
    const getStatus = () => {
      let formDataList: Array<any> = handleEmpty(state.formData)
      switch (state.mode) {
        case 'form_data':
          return formDataList.length > 0
        case 'raw':
          return state.rawData !== ''
      }
    }

    // 获取表单数据
    const getData = () => {
      let requestData: any = {}
      requestData.mode = state.mode
      if (state.mode === 'raw') {
        requestData.data = state.rawData
        requestData.language = state.language
      }

      if (state.mode === 'form_data') {
        requestData.data = state.formData
      }
      return requestData
    }

    // 参数类型变更
    const radioChange = (value: any) => {
      state.mode = value
      state.popoverOpen = false
      handleHeader()
    }

    // 处理raw 语言
    const handleLanguage = (language: any) => {
      state.popoverOpen = !state.popoverOpen
      rawPopoverRef.value.hide()
      state.language = language
      handleHeader()
    }

    // 处理头信息
    const handleHeader = (remove: any = false) => {
      let headerData: any
      if (state.mode === 'raw') {
        if (state.language.toLowerCase() === 'text') {
          headerData = {key: "Content-Type", value: "text/plain"}
        } else if (state.language.toLowerCase() === 'json') {
          headerData = {key: "Content-Type", value: "application/json"}
        }
      } else if (state.mode === "form_data") {
        remove = true
        headerData = {key: "Content-Type"}
        formDataBlur()
      }
      if (headerData) {
        emit('updateHeader', headerData, remove)
      }
    }

    // 打开语言选择面板
    const showPopover = () => {
      state.popoverOpen = !state.popoverOpen
    }
    // 美化json
    const jsonFormat = () => {
      try {
        state.rawData = monacoEditRef.value.getValue()
        state.rawData = JSON.stringify(JSON.parse(state.rawData), null, 4);
      } catch {
        ElMessage.info('JSON格式错误！')
      }
    }
    // 压缩json
    const jsonCompact = () => {
      try {
        state.rawData = monacoEditRef.value.getValue()
        state.rawData = JSON.stringify(JSON.parse(state.rawData));
      } catch {
        ElMessage.info('JSON格式错误！')
      }
    }

    // bodyData
    const addData = () => {
      state.bodyData.push({key: '', type: 'string', value: ''})
    }
    const deleteData = (index: number) => {
      state.bodyData.splice(index, 1)
    }

    // params
    const addParams = () => {
      state.paramsData.push({key: '', type: 'string', value: ''})
    }
    const deleteParams = (index: number) => {
      state.paramsData.splice(index, 1)
    }

    // formData
    const addFormData = () => {
      state.formData.push({key: '', type: 'text', value: ''})
    }
    // 删除
    const deleteFormData = (index: number) => {
      state.formData.splice(index, 1)
    }
    const formDataBlur = () => {
      if (state.formData.length > 0) {
        let endData = state.formData[state.formData.length - 1]
        if (!endData) {
          addFormData()
        } else if (endData.key !== "" || endData.value !== "") {
          addFormData()
        }
      } else {
        addFormData()
      }
    }

    // 选择文件时触发，上传文件，回写地址
    const fileChange = (e: any, row: any) => {
      state.fileData = e.target.files[0]
      let file: any = e.target.files[0]
      let formData = new FormData
      formData.append('name', file.name)
      formData.append('file', file)
      useFileApi().upload(formData)
          .then((res: any) => {
            row.value = {abspath: res.data.abspath, name: res.data.name}
          })

    }
    // 删除文件处理
    const deletedFile = (row: any, index: number) => {
      let fileRef: any = document.getElementById('selectFile' + index)
      useFileApi().deleted({name: row.value.name})
      row.value = {}
      if (fileRef) fileRef.value = ''
    }

    // 选择文件
    const selectFile = (index: number) => {
      let fileRef = document.getElementById('selectFile' + index)
      if (fileRef) fileRef.click()
    }

    // 监听language 设置 long
    watch(
        () => state.language,
        (val) => {
          if (val.toLowerCase() == 'text') {
            state.long = 'plaintext'
          }
          if (val.toLowerCase() == 'json') {
            state.long = 'json'
          }
        }
    );

    watch(
        () => state.rawData,
        (val) => {
          if (val) {
            handleHeader()
          } else {
            handleHeader(true)
          }
        }, {
          deep: true
        }
    );

    watch(
        () => state.formData,
        () => {
          formDataBlur()
        }, {
          deep: true
        }
    );

    return {
      setData,
      radioChange,
      getData,
      addData,
      deleteData,
      addParams,
      deleteParams,
      deletedFile,
      formDataRef,
      rawPopoverRef,
      monacoEditRef,
      jsonFormat,
      jsonCompact,
      deleteFormData,
      selectFile,
      fileChange,
      addFormData,
      formDataBlur,
      showPopover,
      handleLanguage,
      getStatus,
      ...toRefs(state),
    }
//
  },
});
</script>

<style lang="scss" scoped>

.employee_body {
  margin: 10px 20px 0;
  overflow: hidden;
}

.app-container {
  padding: 0;
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

:deep(.radio-group) {
  margin-bottom: 4px;
}
</style>

<style lang="scss">

.file-input-container {
  display: inline-block;
  max-width: 100%;

  .file-input {
    display: flex;
    align-items: center;
    padding: var(--spacing-xs);

    .file-input__native {
      opacity: 0;
      position: absolute;
      width: 0;
      height: 0;
      pointer-events: none;
    }

    .file-input__fake {
      position: relative;
      height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;
      background-color: #F2F2F2;
      min-width: 100px;
      color: #6B6B6B;
      font-weight: 600;

      &:hover {
        color: #212121;
        background-color: #E6E6EE;
      }
    }

    .btn {
      box-sizing: border-box;
      border-radius: 4px;
    }

    .file-input__name {
      box-sizing: border-box;
      display: flex;
      min-width: 0;
      height: 24px;
      align-items: center;
      border-radius: 4px;
      border: 1px solid #E6E6E6;
      font-size: 12px;
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica, Arial, sans-serif;
      color: #212121;
      background-color: transparent;
      padding: 4px 2px;

      .file-input__name__title {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .file-input__name__delete-icon {
        display: flex;
        align-items: center;
        margin-left: 8px;
        padding-right: 2px;
        cursor: pointer;
        color: #212121;
      }
    }
  }
}

.dropdown-menu {
  padding: 4px 0;
  box-sizing: border-box;
  background-color: #F9F9F9;
  border-radius: 4px;
  border: 1px solid #EDEDED;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.2);

  .dropdown-menu-item {
    position: relative;
    box-sizing: border-box;
    height: 32px;
    color: #212121;
    font-size: 12px;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica, Arial, sans-serif;;
    display: flex;
    align-items: center;
    cursor: default;
    -webkit-user-select: none;
    user-select: none;
    padding: 0 16px;

    span {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    &:hover {
      background-color: #EDEDED;
    }
  }
}


</style>
<style>
.popover-class {
  padding: 0 !important;
}
</style>