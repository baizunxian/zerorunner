<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        :title="state.editType === 'save'? '新增菜单' : '修改菜单'"
        v-model="state.isShowDialog"
        width="769px">
      <el-form :model="state.form" :rules="state.rules" size="default" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="上级菜单" prop="parent_id">
              <el-select v-model="state.form.parent_id" clearable placeholder="Select">
                <el-option :value="0" label="根目录"></el-option>
                <el-option
                    v-for="item in allMenuList"
                    :key="item.id"
                    :label="item.title"
                    :value="item.id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="菜单类型" prop="menu_type">
              <el-radio-group v-model="state.form.menu_type">
                <el-radio :label="10">菜单</el-radio>
                <el-radio :label="20">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="菜单名称" prop="title">
              <el-input v-model="state.form.title" placeholder="格式：message.router.xxx" clearable></el-input>
            </el-form-item>
          </el-col>
          <template v-if="state.form.menu_type === 10">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="路由名称" prop="name">
                <el-input v-model="state.form.name" placeholder="路由中的 name 值" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="路由路径" prop="path">
                <el-input v-model="state.form.path" placeholder="路由中的 path 值" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="重定向">
                <el-input v-model="state.form.redirect" placeholder="请输入路由重定向" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="菜单图标">
                <IconSelector placeholder="请输入菜单图标" v-model="state.form.icon" type="all"/>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="组件路径" prop="component">
                <el-input v-model="state.form.component" placeholder="组件路径" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="链接地址">
                <el-input v-model="state.form.isLink" placeholder="外链/内嵌时链接地址（http:xxx.com）" clearable
                          :disabled="!state.form.isLink">
                </el-input>
              </el-form-item>
            </el-col>
            <!--            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">-->
            <!--              <el-form-item label="权限标识">-->
            <!--                <el-select v-model="form.roles" placeholder="取角色管理" clearable class="w100">-->
            <!--                  <el-option label="admin" value="admin"></el-option>-->
            <!--                  <el-option label="common" value="common"></el-option>-->
            <!--                </el-select>-->
            <!--              </el-form-item>-->
            <!--            </el-col>-->
          </template>
          <template v-if="state.form.menuType === 'btn'">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="权限标识">
                <el-input v-model="state.form.btnPower" placeholder="请输入权限标识" clearable></el-input>
              </el-form-item>
            </el-col>
          </template>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="菜单排序">
              <el-input-number v-model="state.form.sort" controls-position="right" placeholder="请输入排序" class="w100"/>
            </el-form-item>
          </el-col>
          <template v-if="state.form.menu_type === 10">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否隐藏">
                <el-radio-group v-model="state.form.isHide">
                  <el-radio :label="1">隐藏</el-radio>
                  <el-radio :label="0">不隐藏</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="页面缓存">
                <el-radio-group v-model="state.form.isKeepAlive">
                  <el-radio :label="1">缓存</el-radio>
                  <el-radio :label="0">不缓存</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否固定">
                <el-radio-group v-model="state.form.isAffix">
                  <el-radio :label="1">固定</el-radio>
                  <el-radio :label="0">不固定</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否外链">
                <el-radio-group v-model="state.form.isLink" :disabled="state.form.isIframe">
                  <el-radio :label="1">是</el-radio>
                  <el-radio :label="0">否</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否内嵌">
                <el-radio-group v-model="state.form.isIframe" @change="onSelectIframeChange">
                  <el-radio :label="1">是</el-radio>
                  <el-radio :label="0">否</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </template>
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

<script lang="ts" setup name="SaveOrUpdateMenu">
import {onMounted, reactive} from 'vue';
import IconSelector from '/@/components/iconSelector/index.vue';
import {useMenuApi} from "/@/api/useSystemApi/menu";
import {ElMessage} from "element-plus";

const emit = defineEmits(['getList'])
const props = defineProps({
  allMenuList: {
    type: Array,
  },
  menuList: {
    type: Array,
  }
})

const createMenuForm = () => {
  return {
    id: null, // 上级菜单
    parent_id: 0, // 上级菜单
    menu_type: 10, // 菜单类型  10 菜单  20 按钮
    name: '', // 路由名称
    meta: {},
    component: '', // 组件路径
    sort: 0, // 菜单排序
    path: '', // 路由路径
    redirect: '', // 路由重定向，有子集 children 时
    title: '', // 菜单名称
    icon: '', // 菜单图标
    isHide: 0, // 是否隐藏
    isKeepAlive: 1, // 是否缓存
    isAffix: 0, // 是否固定
    isLink: 0, // 外链/内嵌时链接地址（http:xxx.com），开启外链条件，`1、isLink:true 2、链接地址不为空`
    isIframe: 1, // 是否内嵌，开启条件，`1、isIframe:true 2、链接地址不为空`
    roles: '', // 权限标识，取角色管理
    btnPower: '', // 菜单类型为按钮时，权限标识
  }
}

const state = reactive({
  isShowDialog: false,
  editType: '',
  // 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式
  form: createMenuForm(),
  rules: {
    name: [{required: true, message: '请输入路由名称', trigger: 'blur'},],
    parent_id: [{required: true, message: '请选择上级菜单', trigger: 'blur'},],
    menu_type: [{required: true, message: '请选择菜单类型', trigger: 'blur'},],
    component: [{required: true, message: '请输入组件路径', trigger: 'blur'},],
    path: [{required: true, message: '请输入路由路径', trigger: 'blur'},],
    title: [{required: true, message: '请输入菜单名称', trigger: 'blur'},],
  },
  menuData: [], // 上级菜单数据
});
// 创建表单

// 打开弹窗
const openDialog = (editType: string, row: any) => {
  state.editType = editType
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
  } else {
    state.form = createMenuForm()
  }
  state.isShowDialog = true;
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 是否内嵌下拉改变
const onSelectIframeChange = () => {
  if (state.form.meta.isIframe) state.form.isLink = true;
  else state.form.isLink = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};
// 新增
const saveOrUpdate = () => {
  useMenuApi().saveOrUpdate(state.form)
      .then(() => {
        ElMessage.success('操作成功');
        emit('getList')
        closeDialog(); // 关闭弹窗
      })
  console.log(state.form, 'state.menuForm')
  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};
// 页面加载时
onMounted(() => {
  console.log(props.allMenuList,11111111)
  // getMenuData();
});


defineExpose({
  openDialog,
})

</script>
