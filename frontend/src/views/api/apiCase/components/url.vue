<template>
  <div>
    <el-form
        :inline="true"
        ref="formRef"
        :model="form"
        label-width="50px"
        label-position="right"
        :rules="rules"
        class="title">
      <el-row :gutter="35">
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
          <el-form-item prop="url">
            <el-input
                v-model="form.url"
                placeholder="请输入请求路径"
                class="input-with-select"
                style="min-width:600px"
            >
              <template #prepend>
                <el-select v-model="form.method" placeholder="Select" style="width: 100px">
                  <el-option
                      v-for="item in methodList"
                      :key="item"
                      :label="item"
                      :value="item">
                    <span style="float: left; font-weight: 200">{{ item }}</span>
                  </el-option>
                </el-select>
              </template>
            </el-input>
          </el-form-item>

<!--          <el-button type="primary" @click="saveOrUpdateCase('save')" class="title-button">保存</el-button>-->
<!--          <el-button type="success" @click="saveOrUpdateCase('debug')">调试</el-button>-->
          <!--          <el-button type="warning">断言调试</el-button>-->
        </el-col>
      </el-row>

    </el-form>

    <el-dialog
        draggable
        v-model="showEnv"
        width="600px"
        top="8vh"
        :close-on-click-modal="false">
      <el-form
          :model="form"
          label-width="80px"

      >
        <el-form-item label="运行环境" prop="base_url">
          <el-select v-model="form.base_url" placeholder="选择环境" filterable style="width:80%">
            <el-option value="" label="自带环境"></el-option>
            <el-option
                v-for="item in envList"
                :key="item.id"
                :label="item.name"
                :value="item.url">
              <span style="float: left">{{ item.name }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
            <span class="dialog-footer">
              <el-button @click="showEnv = !showEnv">取消</el-button>
              <el-button type="primary" @click="saveOrUpdateCase('debug')">调试</el-button>
            </span>
      </template>
    </el-dialog>

  </div>
</template>

<script lang="ts">
import {defineComponent, reactive, ref, toRefs} from "vue";
import {ElMessage} from "element-plus";
import {useStore} from '/@/store';


interface formRow {
  id: any,
  url: string,
  method: string,
  base_url: any,
  enabled_flag: any
}

export default defineComponent({
  name: 'case-url',
  components: {},
  setup(props, {emit}) {
    const formRef = ref()
    const store = useStore();
    const createForm = () => {
      return {
        id: '',
        url: '',
        method: 'POST',
        base_url: '',
        env_id: null,
      }
    }
    const state = reactive({
      isShowDialog: false,
      handleType: '',   //apiCase 调用类型， 保存，调试
      methodList: ['POST', 'GET', 'PUT', 'HEAD', 'DELETE', 'OPTIONS'],
      // 表单及校验
      form: createForm(),
      rules: {
        url: [{required: true, message: '请求地址不能为空', trigger: 'blur'}],
      },
      // env
      showEnv: false,
      envList: [],

    });
    // 初始化表单
    const setData = (data: formRow) => {
      state.form = createForm()
      if (data) state.form = data
    }

    // 获取表单数据
    const getData = () => {
      return state.form
    }
    // 保存，或调试用例
    const saveOrUpdateCase = (handleType: string = 'save') => {
      formRef.value.validate((valid: any) => {
        if (valid) {
          if (handleType === 'save') {
            emit('saveOrUpdateOrDebug', 'save')
          } else if (handleType === 'debug') {
            if (!store.state.env.envId) {
              ElMessage.warning("请选择运行环境！")
              return
            }
            emit('saveOrUpdateOrDebug', 'debug')
          }
        } else {
          ElMessage.warning('请填写请求地址信息');
        }
      })
    }

    return {
      formRef,
      setData,
      getData,
      saveOrUpdateCase,
      ...toRefs(state),
    };
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

.title {
  margin-left: 10px;
  margin-top: 10px;

  .title-button {
    margin-left: 10px;
  }

  :deep(.el-input-group__prepend) {
    // color: #909399;
    font-weight: 1000;
  }

  //::v-deep .el-input__inner {
  //  font-weight: bold;
  //  font-size: 13px;
  //}

  :deep(.el-form-item--mini .el-form-item__error) {
    padding-left: 100px;
  }

  :deep(.el-form-item--mini.el-form-item, .el-form-item--small.el-form-item) {
    margin-bottom: 5px;
  }
}

.tip {
  padding: 4px 4px;
  border-left: 5px solid #409EFF;
  margin-top: 20px;

  p {
    margin: 0;
  }
}

/* el-input */
:deep(.el-input__inner) {
  font-weight: bold;
}
</style>
