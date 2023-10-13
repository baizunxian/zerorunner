<template>
  <ValidatorsController :data="state.validators"></ValidatorsController>
</template>

<script setup name="ApiValidators">
import {reactive} from "vue";
import {handleEmpty} from "/@/utils/other";
import ValidatorsController from "/@/components/Z-StepController/validators/ValidatorsController.vue"

const state = reactive({
  // headers
  validators: [],  // 请求头数据

});
// 初始化数据
const setData = (data) => {
  state.validators = data ? data : []
}

// 获取表单数据
const getData = () => {
  state.validators.forEach((e, index) => {
    const indexNumber = index + 1
    if (e.mode === "") {
      throw new Error(`断言: 第${indexNumber}行 断言类型不能为空~🤣`)
    }
    if (e.check === "") {
      throw new Error(`断言: 第${indexNumber}行 提取表达式不能为空~🤣`)
    }
    if (e.expect === "") {
      throw new Error(`断言: 第${indexNumber}行 期望值不能为空~🤣`)
    }
    if (e.continue_extract && (e.continue_index === "" || e.continue_index === null)) {
      throw new Error(`断言: 第${indexNumber}行 请填写提取下标~🤣`)
    }
  })
  return handleEmpty(state.validators)
}

const getDataLength = () => {
  return state.validators.length
}

defineExpose({
  setData,
  getData,
  getDataLength,
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