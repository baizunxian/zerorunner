<template>
  <div class="system-edit-role-container">
    <el-dialog
        draggable :title="state.editType === 'save'? `新增` : `修改`" v-model="state.isShowDialog" width="769px">
      <el-form :model="state.form" :rules="state.rules" label-width="90px" ref="formRef">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色名称" prop="name">
              <el-input v-model="state.form.name" placeholder="请输入角色名称" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色标识" prop="role_type">
              <template #label>
                <el-tooltip effect="dark" content="用于 `router/route.ts` meta.roles" placement="top-start">
                  <span>角色标识</span>
                </el-tooltip>
              </template>
              <el-select v-model="state.form.role_type" clearable placeholder="角色标识">
                <el-option
                    v-for="item in [{role_type: 10, label:'菜单权限'}]"
                    :key="item.role_type"
                    :label="item.label"
                    :value="item.role_type"
                >
                </el-option>
              </el-select>
              <!--              <el-input v-model="form.role_type" placeholder="请输入角色标识" clearable></el-input>-->
            </el-form-item>
          </el-col>
          <!--          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">-->
          <!--            <el-form-item label="排序">-->
          <!--              <el-input-number v-model="ruleForm.sort" :min="0" :max="999" controls-position="right" placeholder="请输入排序"-->
          <!--                               class="w100"/>-->
          <!--            </el-form-item>-->
          <!--          </el-col>-->
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色状态">
              <el-switch v-model="state.form.status" :active-value="10" :inactive-value="20" inline-prompt
                         active-text="启"
                         inactive-text="禁"></el-switch>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="角色描述">
              <el-input v-model="state.form.description" type="textarea" placeholder="请输入角色描述"
                        maxlength="150"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="菜单权限">
              <el-tree ref="roleTreeRef"
                       :data="state.menuData"
                       :props="state.menuProps"
                       @check-change="roleTreeChange"
                       :default-checked-keys="state.form.menus"
                       node-key="id"
                       show-checkbox class="menu-data-tree"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel">取 消</el-button>
					<el-button type="primary" @click="saveOrUpdate">保 存</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="SaveOrUpdateRole">
import {reactive, ref} from 'vue';
import {useMenuApi} from "/@/api/useSystemApi/menu";
import {useRolesApi} from "/@/api/useSystemApi/roles";
import {ElMessage} from "element-plus";

// 定义接口来定义对象的类型
interface MenuDataTree {
  id: number;
  title: string;
  children?: MenuDataTree[];
}

interface RoleData {
  id: string | number | null;
  name: string;
  role_type: number;
  menus: Array<number>;
  description: string;
  status: boolean;
}

interface RoleState {
  isShowDialog: boolean;
  editType: any;
  form: RoleData;
  rules: Object;
  menuData: Array<MenuDataTree>;
  menuProps: {
    children: string;
    label: string;
  };
}

const emit = defineEmits(['getList'])

let createForm = () => {
  return {
    id: null,  //
    name: '',  // 角色名称
    role_type: 10,   // 角色类型
    menus: [],    // 关联菜单
    description: '',   //描述
    status: 10,   // 角色状态 10 启用，20 禁用
  }
}
const formRef = ref()
const roleTreeRef = ref()
const state = reactive<RoleState>({
  editType: null,
  isShowDialog: false,
  form: createForm(),
  menuData: [],
  rules: {
    name: [{required: true, message: '请输入角色名称', trigger: 'blur'},],
    role_type: [{required: true, message: '请选择角色类型', trigger: 'blur'},],
  },
  menuProps: {
    children: 'children',
    label: 'title',
  },
});
// 打开弹窗
const openDialog = (editType: string, row: RoleData) => {
  getMenuData()
  state.editType = editType
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
  } else {
    state.form = createForm()
  }
  state.isShowDialog = true;
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};
// 更新-新增
const saveOrUpdate = () => {
  formRef.value.validate((valid: any) => {
    if (valid) {
      useRolesApi().saveOrUpdate(state.form)
          .then(() => {
            ElMessage.success('操作成功');
            emit('getList')
            closeDialog(); // 关闭弹窗
          })
    }
  })

}
// 获取菜单结构数据
const getMenuData = () => {
  useMenuApi().getAllMenus()
      .then(res => {
        state.menuData = res.data
      });
}
// 赋值勾选的权限
const roleTreeChange = () => {
  state.form.menus = roleTreeRef.value.getCheckedKeys(true)
}

defineExpose({
  openDialog,

})
</script>

<style scoped lang="scss">
.system-edit-role-container {
  .menu-data-tree {
    border: var(--el-input-border, var(--el-border-base));
    border-radius: var(--el-input-border-radius, var(--el-border-radius-base));
    padding: 5px;
  }
}
</style>
