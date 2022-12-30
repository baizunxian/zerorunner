<template>
  <div class="api-case el-card">
    <el-row>
      <!--      <div class="api-case__ssl">-->
      <!--        <strong :style="{color: form.ssl ? '#409eff' : '', paddingRight: '5px'}">SSL</strong>-->
      <!--        <el-switch-->
      <!--            v-model="form.ssl"-->
      <!--            size="default"-->
      <!--        />-->
      <!--      </div>-->

      <el-col :xs="15" :sm="15" :md="15" :lg="15" :xl="15" class="mb20">
        <div class="api-case__method" style="padding-left: 5px">
          <el-input
              size="default"
              v-model="form.url"
              placeholder="请输入请求路径"
              class="input-with-select"
              style="min-width:400px"
          >
            <template #prepend>
              <el-select v-model="form.method"
                         size="default"
                         ref="methodRef"
                         placeholder=""
                         @change="methodChange"
                         style="width: 100px; color: #22a1c4">
                <el-option
                    v-for="item in methodList"
                    :key="item"
                    :label="item"
                    :value="item">
                  <span :style="{color: getMethodColor(item)}">{{ item }}</span>
                </el-option>
              </el-select>
            </template>
          </el-input>
        </div>
      </el-col>
      <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
        <div class="api-case__operation" style="padding-left: 12px">
          <el-button size="default" type="primary" @click="saveOrUpdateOrDebug('save')" class="title-button">保存
          </el-button>
          <el-button size="default" type="success" @click="saveOrUpdateOrDebug('debug')">调试</el-button>
          <el-button size="default" type="danger" @click="saveOrUpdateOrDebug('debug')">删除</el-button>
        </div>
      </el-col>
      <!--      </div>-->
    </el-row>

    <div class="api-case__detail">
      <el-form ref="formRef"
               :model="form"
               label-width="auto"
               label-position="right"
               :rules="rules">
        <el-row :gutter="24">
          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="用例名称" prop="name" style="width: 100%">
              <el-input size=""
                        v-model.trim="form.name"
                        style="width: 100%;"
                        placeholder="请输入用例名称"></el-input>
            </el-form-item>

          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">

            <el-form-item label="项目/模块" prop="project_id" style="width: 100%">
              <el-cascader v-model="form.project_module"
                           :props="{label:'name', value:'id'}"
                           :options="projectTree"
                           filterable
                           size=""
                           style="width: 100%"
                           @change="projectModuleChange"/>
            </el-form-item>
          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">

            <el-form-item label="用例标签" prop="tag">
              <el-tag
                  v-for="tag in form.tags"
                  :key="tag"
                  size="default"
                  type="success"
                  closable
                  style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                  :disable-transitions="false"
                  @close="removeTag(tag)"
              >{{ tag }}
              </el-tag>

              <el-input
                  v-if="editTag"
                  ref="caseTagInputRef"
                  v-model="tagValue"
                  class="ml-1 w-20"
                  size="small"
                  @keyup.enter="addTag"
                  @blur="addTag"
                  style="width: 100px"
              />
              <el-button v-else size="small" @click="showEditTag">
                + New Tag
              </el-button>
            </el-form-item>

          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="描述" prop="" style="width: 100%;">
              <el-input size="default"
                        type="textarea"
                        v-model.trim="form.remarks"
                        style="width: 100%;"
                        placeholder="请输入用例名称"></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">

          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="创建用户" prop="" style="width: 100%;">
              <strong>{{ form.created_by_name }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="创建时间" prop="" style="width: 100%;">
              <strong>{{ form.creation_date }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="更新用户" prop="" style="width: 100%;">
              <strong>{{ form.updated_by_name }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="更新时间" prop="" style="width: 100%;">
              <strong>{{ form.updation_date }}</strong>
            </el-form-item>
          </el-col>

        </el-row>
      </el-form>
    </div>

  </div>
</template>

<script lang="ts">
import {useProjectApi} from '/@/api/useAutoApi/project'
import {useModuleApi} from '/@/api/useAutoApi/module'
import {defineComponent, onMounted, reactive, ref, toRefs, nextTick} from "vue";
import {useEnvApi} from "/@/api/useAutoApi/env";
import {getMethodColor} from "/@/utils/case"
import {ElMessage} from "element-plus";
import {useStore} from "/@/store";


export default defineComponent({
  name: 'caseInfo',
  components: {},
  setup(props, {emit}) {
    const formRef = ref()
    const methodRef = ref()
    const caseTagInputRef = ref()
    const store = useStore();
    const createForm = () => {
      return {
        id: null,
        method: '',
        name: '',
        url: '',
        ssl: false,
        code_id: null,
        code: '',
        project_module: [],
        project_id: null,
        module_id: null,
        tags: [],
        priority: 3,
        remarks: "",
      }
    }
    const state = reactive({
      // cat apiInfo info
      showCaseInfo: false,
      //tag
      editTag: false,
      tagValue: "",
      // form
      isShowDialog: false,
      handleType: '',   //apiInfo 调用类型， 保存，调试
      // 表单及校验
      form: createForm(),
      rules: {
        name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
        project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'}],
        module_id: [{required: true, message: '请选择所属模块', trigger: 'blur'}],
      },
      // project
      projectTree: [],
      projectQuery: {
        page: 1,
        pageSize: 1000,
      },
      // module
      moduleList: [],
      moduleQuery: {
        page: 1,
        pageSize: 1000,
        project_id: null,
      },

      // url
      methodList: ['POST', "GET", "PUT", "DELETE"],

      // env
      envList: []


    });
    // 初始化表单
    const setData = (formData: any) => {
      state.form = createForm()
      if (formData) {
        state.form = {...createForm(), ...formData}
        state.form.project_module = [state.form.project_id, state.form.module_id]
        if (!state.form.tags) state.form.tags = []
        if (formData.project_id) {
          state.moduleQuery.project_id = formData.project_id
          getModuleList()
        }
        methodChange(state.form.method)
      }
    }

    // 获取表单数据
    const getData = () => {
      return state.form
    }
    //  ----------------project start-------------------------------------
    // 获取项目列表
    const getProjectTree = () => {
      useProjectApi().getTree({})
          .then(res => {
            state.projectTree = res.data
          })
    }
    // 选择项目
    const selectProject = (project_id: any) => {
      state.form.module_id = null
      state.moduleList = []
      state.moduleQuery.project_id = project_id

      getModuleList()
    }
    //  ----------------module start-------------------------------------
    // 获取模块列表
    const getModuleList = () => {
      useModuleApi().getList(state.moduleQuery)
          .then(res => {
            state.moduleList = res.data.rows
          })
    }

    // 初始化env
    const getEnvList = () => {
      useEnvApi().getList({page: 1, pageSize: 1000})
          .then(res => {
            state.envList = res.data.rows
          })
    };

    // methodChange
    const methodChange = (method: string) => {
      let selectInputEl = methodRef.value.$el.getElementsByTagName("input")
      if (selectInputEl.length > 0) selectInputEl[0].style.color = getMethodColor(method)
    }

    // handlePojectModuleChange

    const projectModuleChange = (value: any) => {
      state.form.project_id = value[0]
      state.form.module_id = value[1]
    }

    // tags
    const showEditTag = () => {
      state.editTag = true
      nextTick(() => {
        caseTagInputRef.value!.input!.focus()
      })
    }

    const addTag = () => {
      if (state.editTag && state.tagValue) {
        if (!state.form.tags) state.form.tags = []
        state.form.tags.push(state.tagValue)
      }
      state.editTag = false
      state.tagValue = ''
    }
    const removeTag = (tag: string) => {
      state.form.tags.splice(state.form.tags.indexOf(tag), 1)
    }

    // 保存，或调试用例
    const saveOrUpdateOrDebug = (handleType: string = 'save') => {
      formRef.value.validate((valid: any) => {
        if (valid) {
          if (handleType === 'save') {
            emit('saveOrUpdateOrDebug', 'save')
          } else if (handleType === 'debug') {
            emit('saveOrUpdateOrDebug', 'debug')
          }
        } else {
          ElMessage.warning('请填写请求地址信息');
        }
      })
    }

    onMounted(() => {
      getProjectTree()
      getEnvList()
    })
    return {
      formRef,
      methodRef,
      caseTagInputRef,
      setData,
      getData,
      getProjectTree,
      getModuleList,
      selectProject,
      getMethodColor,
      methodChange,
      projectModuleChange,
      addTag,
      removeTag,
      showEditTag,
      saveOrUpdateOrDebug,
      ...toRefs(state),
    };
  },
});
</script>


<style lang="scss" scoped>

.api-case {
  padding: 15px 16px;
  background-color: #ffffff;
  border-radius: 10px;
  border-left: 5px solid #409eff;
  margin-bottom: 20px;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);

  .api-case__url_info {
    display: flex;
    margin-bottom: 20px;
  }

  :deep(.input-with-select .el-input-group__prepend) {
    background-color: var(--el-fill-color-blank);
  }
}
</style>