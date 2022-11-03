<template>
  <headers-controller :data="headers"></headers-controller>
</template>

<script lang="ts">
import {defineComponent, reactive, toRefs} from "vue";
import headersController from "/@/components/StepController/headersController.vue";
import {handleEmpty} from "/@/utils/other";

interface baseState {
  key: string,
  value: string,
  remarks: string
}

interface headersState {
  headers: Array<baseState>,
}


export default defineComponent({
  name: 'requestHeaders',
  components: {headersController},
  setup() {
    const state = reactive<headersState>({
      // headers
      headers: [],  // 请求头数据

    });
    // 初始化数据
    const setData = (data: any) => {
      state.headers = data ? data : []
    }

    // 获取表单数据
    const getData = () => {
      return handleEmpty(state.headers)
    }

    // 获取是否填写状态
    const getStatus = () => {
      return handleEmpty(state.headers).length > 0
    }

    // updateHeader {key: "Content-Type", value: "application/json"} //更新请求头
    const updateHeader = (headerData: any, remove: any = false) => {
      let headerInfo = state.headers.find(e => headerData?.key && headerData.key.toLowerCase() === e.key.toLowerCase())
      if (headerInfo) {
        state.headers.forEach((e: any, index: number) => {
          if (headerData?.key && headerData.key.toLowerCase() === e.key.toLowerCase()) {
            state.headers.splice(index, 1)
            if (!remove) {
              state.headers.unshift(headerData)
            }
          }
        })
      } else {
        if (!remove) {
          state.headers.unshift(headerData)
        }
      }

    }


    return {
      setData,
      getData,
      updateHeader,
      getStatus,
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