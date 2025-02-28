<template>
  <div class="api-case el-card">
    <div class="api-case__detail">
      <el-form ref="formRef"
               :model="state.form"
               label-width="auto"
               label-position="right"
               :rules="state.rules">
        <el-row>
          <el-col :span="24">
            <el-form-item label="页面名称" prop="name" size="default">
              <el-col :xs="10" :sm="10" :md="10" :lg="10" :xl="10" class="mb20">
                <div class="api-case__method">
                  <el-input
                      size="default"
                      v-model="state.form.name"
                      placeholder="请输入页面名称"
                  >
                  </el-input>
                </div>
              </el-col>
              <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
                <div class="api-case__operation" style="padding-left: 12px">
                  <el-button size="default" type="primary" @click="savePage" class="title-button">保存
                  </el-button>
                </div>
              </el-col>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="页面地址" prop="url">
              <el-input v-model.trim="state.form.url"
                        style="width: 100%;"
                        clearable
                        placeholder="请输入页面地址"></el-input>
            </el-form-item>

          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">

            <el-form-item label="项目/模块" prop="project_id">
              <el-cascader v-model="state.form.project_module"
                           placeholder="请选择项目/模块"
                           :props="{label:'name', value:'id'}"
                           :options="state.projectTree"
                           filterable
                           style="width: 100%"
                           @change="projectModuleChange"/>
            </el-form-item>
          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">

            <el-form-item label="页面标签" prop="tag">
              <el-tag
                  v-for="tag in state.form.tags"
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
                  v-if="state.editTag"
                  ref="tagInputRef"
                  v-model="state.tagValue"
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
            <el-form-item label="描述" prop="">
              <el-input size="default"
                        type="textarea"
                        v-model.trim="state.form.remarks"
                        style="width: 100%;"
                        placeholder="描述"></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">

          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="创建用户" prop="">
              <strong>{{ state.form.created_by_name }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="创建时间" prop="">
              <strong>{{ state.form.creation_date }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="更新用户" prop="" style="width: 100%;">
              <strong>{{ state.form.updated_by_name }}</strong>
            </el-form-item>
          </el-col>

          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6" class="mb20">
            <el-form-item label="更新时间" prop="" style="width: 100%;">
              <strong>{{ state.form.updation_date }}</strong>
            </el-form-item>
          </el-col>

        </el-row>
      </el-form>
    </div>

  </div>
</template>

<script setup name="EditPage">
import {ElButton, ElMessage} from "element-plus";
import {nextTick, onMounted, reactive, ref, watch} from "vue";
import {useUiPageApi} from "/@/api/useUiApi/uiPage";
import {useProjectApi} from "/@/api/useAutoApi/project";
import {useModuleApi} from "/@/api/useAutoApi/module";

const emit = defineEmits(["update:data"]);

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

const tagInputRef = ref()

const state = reactive({
  form: {},
  rules: {
    name: [{required: true, message: '请输入用例名', trigger: 'blur'}],
    project_id: [{required: true, message: '请选择所属项目', trigger: 'blur'}],
    // env_id: [{required: true, message: '请选择运行环境', trigger: 'blur'}],
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

  //tag
  editTag: false,
  tagValue: "",
});

// tags
const showEditTag = () => {
  state.editTag = true
  nextTick(() => {
    tagInputRef.value?.input.focus()
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
const removeTag = (tag) => {
  state.form.tags.splice(state.form.tags.indexOf(tag), 1)
}

//  ----------------project start-------------------------------------
// 获取项目列表
const getProjectTree = () => {
  useProjectApi().getTree({})
      .then(res => {
        state.projectTree = res.data
      })
}
const projectModuleChange = (value) => {
  state.form.project_id = value ? value[0] : ""
  state.form.module_id = value ? value[1] : ""
}
// 选择项目
const selectProject = (project_id) => {
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

const savePage = () => {
  useUiPageApi().saveOrUpdate(state.form).then((res) => {
    state.form = res.data
    emit("update:data", state.form)
    ElMessage.success("保存成功")
  })
}

onMounted(() => {
  getProjectTree()
})

watch(
    () => props.data,
    (val) => {
      let newData = JSON.parse(JSON.stringify(val))
      newData.project_module = [newData.project_id, newData.module_id]
      state.form = newData
    },
    {
      deep: true,
    }
);

</script>

<style scoped lang="scss">

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