<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <div class="system-menu-search mb15">
        <el-input v-model="listQuery.name" placeholder="请输入菜单名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="getList">
          <el-icon>
            <ele-Search/>
          </el-icon>
          查询
        </el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
          <el-icon>
            <ele-FolderAdd/>
          </el-icon>
          新增菜单
        </el-button>
      </div>
      <el-table
          border
          :data="menuList"
          v-loading="menuTableLoading"
          style="width: 100%"
          row-key="path"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }">

        <el-table-column
            v-for="field in fieldData"
            :key="field.fieldName"
            :label="field.label"
            :align="field.align"
            :width="field.width"
            :show-overflow-tooltip="field.show"
            :prop="field.fieldName"
        >
          <template #default="{row}">
            <template v-if="field.fieldName === 'title'">
              <SvgIcon :name="row.icon"/>
              <span class="ml10">{{ row.title }}</span>
<!--              <el-button size="small"-->
<!--                         type="primary" link-->
<!--                         class="ml10"-->
<!--                         @click="onOpenSaveOrUpdate('update', row)">-->
<!--                {{ row[field.fieldName] }}-->
<!--              </el-button>-->
            </template>

            <template v-else-if="field.fieldName === 'menu_type'">
              <el-tag type="success" v-if="row.menu_type === 10">菜单</el-tag>
              <el-tag type="info" v-else>按钮</el-tag>
            </template>

            <template v-else>
              {{ row[field.fieldName] }}
            </template>

          </template>
        </el-table-column>

        <el-table-column label="操作" show-overflow-tooltip width="140" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="onOpenSaveOrUpdate('update', scope.row)">修改</el-button>
            <el-button size="small" type="primary" link @click="deleted(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <save-or-update :moduleName="moduleName" :menuList="menuList" :allMenuList="allMenuList" @getList="getList"
                    ref="saveOrUpdateRef"/>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, reactive, ref, toRefs} from 'vue';
import {useMenuApi} from '/@/api/useSystemApi/menu';
import {RouteRecordRaw} from 'vue-router';
import {ElMessage, ElMessageBox} from 'element-plus';
import saveOrUpdate from '/@/views/system/menu/components/saveOrUpdate.vue';

export default defineComponent({
  name: 'systemMenu',
  components: {saveOrUpdate},
  setup() {
    const saveOrUpdateRef = ref();
    const state = reactive({
      fieldData: [
        {fieldName: 'title', label: '菜单名称', width: '', align: 'left', show: true},
        {fieldName: 'path', label: '路由路径', width: '', align: 'left', show: true},
        {fieldName: 'component', label: '组件路径', width: '', align: 'left', show: true},
        {fieldName: 'roles', label: '权限标识', width: '', align: 'left', show: true},
        {fieldName: 'name', label: '路由名称', width: '', align: 'left', show: true},
        {fieldName: 'sort', label: '排序', width: '', align: 'left', show: true},
        {fieldName: 'menu_type', label: '类型', width: '', align: 'left', show: true},
        // {fieldName: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true},
        // {fieldName: 'updated_by', label: '更新人', width: '', align: 'center', show: true},
        // {fieldName: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true},
        // {fieldName: 'created_by', label: '创建人', width: '', align: 'center', show: true},
      ],
      // list
      moduleName: '菜单', // 模块名称
      menuList: [],
      allMenuList: null,
      menuTableLoading: false,
      listQuery: {
        page: 1,
        pageSize: 200,
        name: '',
      },
    });

    // 递归组装菜单
    const menuAssembly = (parent_menu: Array<object>, all_menu: Array<object>) => {
      parent_menu.forEach(parent => {
        all_menu.forEach(menu => {
          if (menu.parent_id == parent.id) {
            parent.children = parent.children ? parent.children : [];
            parent.children.push(menu);
          }
        })
        if (parent.children) menuAssembly(parent.children, all_menu);
      })
      state.menuList = parent_menu
    };

    // 获取菜单列表
    const getList = async () => {
      state.menuTableLoading = true
      let res = await useMenuApi().allMenu({})
      state.allMenuList = res.data
      let parent_menu = []
      res.data.forEach(menu => {
        if (!menu.parent_id) {
          parent_menu.push(menu)
        }
      })
      menuAssembly(parent_menu, res.data)
      state.menuTableLoading = false
    };
    // 打开新增菜单弹窗
    // const onOpenAddMenu = () => {
    //   addMenuRef.value.openDialog();
    // };
    // 打开编辑菜单弹窗
    const onOpenSaveOrUpdate = (editType: string, row: RouteRecordRaw) => {
      saveOrUpdateRef.value.openDialog(editType, row);
    };
    // 删除当前行
    const deleted = (row: RouteRecordRaw) => {
      ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      })
          .then(() => {
            ElMessage.success('删除成功');
          })
          .catch(() => {
          });
    };
    onMounted(() => {
      getList()
    })

    return {
      // addMenuRef,
      saveOrUpdateRef,
      // onOpenAddMenu,
      onOpenSaveOrUpdate,
      deleted,
      getList,
      ...toRefs(state),
    };
  },
});
</script>

