<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        title="覆盖率报告" v-model="state.isShowDialog"
        width="40%">
      <el-form ref="formRef" :model="state.form" :rules="state.rules" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="报告名称" prop="report_name">
              <el-input v-model="state.form.name" placeholder="报告名称" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="报告类型" prop="name">
              <el-radio-group v-model="state.form.report_type" @click.stop>
                <el-radio :label="10" disabled>全量</el-radio>
                <el-radio :label="20">增量</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <div
                class="h100"
                style=" width:100%; display: flex; justify-content: space-between;">
              <el-card style="width: 45%">
                <div class="mb10" style="justify-content: space-between">
                  <el-tag type="warning">基准分支</el-tag>
                </div>

                <el-select v-model="state.form.old_branches" @change="(val) => getCommitId(val, 'old')"
                           style="width: auto">
                  <el-option v-for="item in state.branches" :key="item.name" :label="item.name"
                             :value="item.name"></el-option>
                </el-select>

                <!--                <el-tag type="">commitId: {{ getCommitId('new') }}</el-tag>-->


              </el-card>

              <div style="position: relative;">
                <el-icon style="transform: rotate(90deg); color: black;">
                  <ele-Sort/>
                </el-icon>
              </div>


              <el-card style="width: 45%">
                <div class="mb10">
                  <el-tag type="success">比对分支</el-tag>
                </div>

                <el-select v-model="state.form.new_branches" @change="(val) => getCommitId(val, 'new')"
                           style="width: auto">
                  <el-option v-for="item in state.branches"
                             :key="item.name"
                             :label="item.name"
                             :value="item.name"></el-option>
                </el-select>

              </el-card>
              <!--                <div>-->
              <!--                  <div style="display: flex">-->
              <!--                    <el-tag type="warning">基准分支</el-tag>-->
              <!--                    <el-select v-model="state.form.old_branches" style="width: auto">-->
              <!--                      <el-option v-for="item in state.branches" :key="item.name" :label="item.name"-->
              <!--                                 :value="item.name"></el-option>-->
              <!--                    </el-select>-->
              <!--                  </div>-->
              <!--                  <div v-show="state.form.new_last_commit_id">1112</div>-->
              <!--                </div>-->

              <!--                <div>-->
              <!--                  <el-icon style="transform: rotate(90deg); color: black;">-->
              <!--                    <ele-Sort/>-->
              <!--                  </el-icon>-->
              <!--                </div>-->

              <!--                <div>-->
              <!--                  <el-tag type="success">比对分支</el-tag>-->
              <!--                  <el-select v-model="state.form.new_branches" style="width: auto">-->
              <!--                    <el-option v-for="item in state.branches" :key="item.name" :label="item.name"-->
              <!--                               :value="item.name"></el-option>-->
              <!--                  </el-select>-->
              <!--                  <div >commit_id: {{state.form.old_last_commit_id}}</div>-->
              <!--                </div>-->
            </div>


            <!--            </el-form-item>-->
          </el-col>


        </el-row>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel">取 消</el-button>
					<el-button type="primary" @click="coverageStart">提 交</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="saveOrUpdateProject">
import {reactive, ref} from 'vue';
import {ElMessage} from "element-plus";
import {useRepositoryApi} from "/@/api/useCoverageApi/repository";
import {useCoverageReportApi} from "/@/api/useCoverageApi/coverage";

const createForm = () => {
  return {
    name: '', // 报告名称
    new_branches: '', // 比对分支
    new_last_commit_id: '', // newCommitId
    old_branches: '', // 基准分支
    old_last_commit_id: '', // oldCommitId
    git_url: '', // 仓库地址
    report_type: 20, // 报告类型
  }
}
const formRef = ref()
const state = reactive({
  isShowDialog: false,
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入报告名称', trigger: 'blur'},],
  },
  branches: [
    {label: 'master', value: 'master'},
    {label: 'develop', value: 'develop'},
    {label: 'release', value: 'release'},
  ]
});


// 打开弹窗
const openDialog = (row) => {
  state.form = createForm()
  if (row) {
    state.form.name = row.name
    state.form.git_url = row.html_url
  }
  getBranches(row)
  state.isShowDialog = true;
};


const getBranches = (row) => {
  useRepositoryApi().getBranches({id: row.id})
      .then(res => {
        state.branches = res.data
      })
}


// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};


const coverageStart = () => {
  useCoverageReportApi().coverageStart(state.form)
      .then((res) => {
        ElMessage.success('覆盖率开始执行');
      })
}

const getCommitId = (val, type) => {
  let branches = state.branches.find(item => item.name === val)
  if (branches) {
    if (type === 'new') {
      state.form.new_last_commit_id = branches.commit.sha
    } else {
      state.form.old_last_commit_id = branches.commit.sha
    }
  }
}
defineExpose({
  openDialog,
})

</script>
