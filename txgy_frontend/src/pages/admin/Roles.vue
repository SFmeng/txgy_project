<template>
  <div class="admin-roles">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">角色管理</h1>
          <p class="page-subtitle">管理系统角色权限，控制用户访问范围</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="handleAdd" class="primary-btn">
            <el-icon><Plus /></el-icon>
            新增角色
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="角色名称">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入角色名称"
            clearable
            class="search-input"
            prefix-icon="Search"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" class="search-btn">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset" class="reset-btn">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 角色列表 -->
    <el-card class="data-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><UserFilled /></el-icon>
            <span class="header-title">角色列表</span>
            <el-tag type="info" class="count-tag">共 {{ pagination.total }} 个角色</el-tag>
          </div>
        </div>
      </template>

      <div class="table-container">
        <el-table :data="roleList" style="width: 100%" v-loading="loading">
          <el-table-column prop="role_name" label="角色名称" width="150" />
          <el-table-column prop="description" label="角色描述" min-width="200" />
          <el-table-column prop="user_count" label="用户数量" width="100" align="center" />
          <el-table-column prop="is_default" label="默认角色" width="100" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_default ? 'success' : 'info'" size="small">
                {{ scope.row.is_default ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="状态" width="80" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'" size="small">
                {{ scope.row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="创建时间" width="160">
            <template #default="scope">
              {{ formatDate(scope.row.create_time) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="360" fixed="right">
            <template #default="scope">
              <div class="action-buttons">
                <el-button
                  size="small"
                  type="primary"
                  @click="handleEdit(scope.row)"
                  class="action-btn edit-btn"
                >
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button
                  size="small"
                  type="warning"
                  @click="handlePermissions(scope.row)"
                  class="action-btn permission-btn"
                >
                  <el-icon><Lock /></el-icon>
                  权限
                </el-button>
                <el-button
                  size="small"
                  type="info"
                  @click="handleMenus(scope.row)"
                  class="action-btn menu-btn"
                >
                  <el-icon><Menu /></el-icon>
                  菜单
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="handleDelete(scope.row)"
                  :disabled="scope.row.is_default"
                  class="action-btn delete-btn"
                  :class="{ 'disabled-btn': scope.row.is_default }"
                >
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <!-- 角色编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        ref="roleFormRef"
        :model="roleForm"
        :rules="roleFormRules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="role_name">
          <el-input v-model="roleForm.role_name" />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="默认角色">
          <el-switch v-model="roleForm.is_default" />
        </el-form-item>
        <el-form-item label="启用状态">
          <el-switch v-model="roleForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 权限分配对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="分配权限"
      width="800px"
    >
      <div class="permission-assignment">
        <div class="role-info">
          <span>角色：{{ currentRole?.role_name }}</span>
        </div>
        <el-tree
          ref="permissionTreeRef"
          :data="permissionTree"
          :props="treeProps"
          show-checkbox
          node-key="perm_id"
          :default-checked-keys="selectedPermissions"
          class="permission-tree"
        >
          <template #default="{ node, data }">
            <span class="tree-node">
              <span>{{ data.perm_name }}</span>
              <span class="node-description">{{ data.description }}</span>
            </span>
          </template>
        </el-tree>
      </div>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePermissionSubmit" :loading="permissionSubmitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 菜单分配对话框 -->
    <el-dialog
      v-model="menuDialogVisible"
      title="分配菜单"
      width="600px"
    >
      <div class="menu-assignment">
        <div class="role-info">
          <span>角色：{{ currentRole?.role_name }}</span>
        </div>
        <el-tree
          ref="menuTreeRef"
          :data="menuTree"
          :props="menuTreeProps"
          show-checkbox
          node-key="menu_id"
          :default-checked-keys="selectedMenus"
          class="menu-tree"
        >
          <template #default="{ node, data }">
            <span class="tree-node">
              <span class="menu-name">{{ data.menu_name }}</span>
              <span class="node-path">{{ data.path }}</span>
            </span>
          </template>
        </el-tree>
      </div>
      <template #footer>
        <el-button @click="menuDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleMenuSubmit" :loading="menuSubmitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, Edit, Delete, Lock, Menu, UserFilled
} from '@element-plus/icons-vue'
import { organizationAPI } from '@/api/organization'
import { useMenuStore } from '@/stores/menu'

// 响应式数据
const loading = ref(false)
const roleList = ref([])
const menuStore = useMenuStore()

// 搜索表单
const searchForm = reactive({
  search: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 角色编辑对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const submitLoading = ref(false)
const roleFormRef = ref()

const roleForm = reactive({
  role_id: '',
  role_name: '',
  description: '',
  is_default: false,
  is_active: true
})

const roleFormRules = {
  role_name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入角色描述', trigger: 'blur' }
  ]
}

// 权限分配对话框
const permissionDialogVisible = ref(false)
const currentRole = ref(null)
const permissionTree = ref([])
const selectedPermissions = ref([])
const permissionSubmitLoading = ref(false)
const permissionTreeRef = ref()

const treeProps = {
  children: 'children',
  label: 'perm_name'
}

// 菜单分配对话框
const menuDialogVisible = ref(false)
const menuTree = ref([])
const selectedMenus = ref([])
const menuSubmitLoading = ref(false)
const menuTreeRef = ref()

const menuTreeProps = {
  children: 'children',
  label: 'menu_name'
}

// 方法
const loadRoleList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.search
    }

    const response = await organizationAPI.getRoles(params)
    roleList.value = response.data.results || []
    pagination.total = response.data.total || 0
  } catch (error) {
    ElMessage.error('加载角色列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadPermissionTree = async () => {
  try {
    const response = await organizationAPI.getPermissions({ group_by_module: true })

    // 转换为树形结构
    const modules = response.data
    permissionTree.value = Object.keys(modules).map(moduleName => ({
      perm_id: `module_${moduleName}`,
      perm_name: moduleName,
      children: modules[moduleName].map(perm => ({
        perm_id: perm.perm_id,
        perm_name: perm.perm_name,
        perm_code: perm.perm_code,
        description: perm.description
      }))
    }))

    console.log('权限树加载完成:', permissionTree.value)
  } catch (error) {
    console.error('加载权限树失败:', error)
    ElMessage.error('加载权限树失败')
  }
}

const loadMenuTree = async () => {
  try {
    const response = await organizationAPI.getMenuTree()
    menuTree.value = response.data || []
  } catch (error) {
    console.error('加载菜单树失败:', error)
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadRoleList()
}

const handleReset = () => {
  searchForm.search = ''
  pagination.page = 1
  loadRoleList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadRoleList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadRoleList()
}

const handleAdd = () => {
  dialogTitle.value = '新增角色'
  isEdit.value = false
  dialogVisible.value = true
  resetRoleForm()
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑角色'
  isEdit.value = true
  dialogVisible.value = true

  nextTick(() => {
    Object.assign(roleForm, {
      role_id: row.role_id,
      role_name: row.role_name,
      description: row.description,
      is_default: row.is_default,
      is_active: row.is_active
    })
  })
}

const handleDelete = async (row) => {
  if (row.is_default) {
    ElMessage.warning('默认角色不能删除')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除角色 "${row.role_name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await organizationAPI.deleteRole(row.role_id)
    ElMessage.success('删除成功')
    loadRoleList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handlePermissions = async (row) => {
  currentRole.value = row
  selectedPermissions.value = [] // 先清空选中的权限
  permissionDialogVisible.value = true

  try {
    // 并行加载权限树和角色权限
    const [treeResponse, roleResponse] = await Promise.all([
      loadPermissionTree(),
      organizationAPI.getRoleDetail(row.role_id)
    ])

    const rolePermissions = roleResponse.data.permissions?.map(p => p.perm_id) || []
    console.log('角色权限ID列表:', rolePermissions)

    // 等待DOM更新
    await nextTick()

    // 设置选中的权限
    selectedPermissions.value = rolePermissions

    // 等待树组件完全渲染后设置选中状态
    setTimeout(() => {
      if (permissionTreeRef.value) {
        permissionTreeRef.value.setCheckedKeys(rolePermissions)
        console.log('权限树自动勾选完成')
      }
    }, 100)

  } catch (error) {
    console.error('获取角色权限失败:', error)
    ElMessage.error('获取角色权限失败')
  }
}

const handleMenus = async (row) => {
  currentRole.value = row
  selectedMenus.value = [] // 先清空选中的菜单
  menuDialogVisible.value = true

  try {
    // 并行加载菜单树和角色菜单
    const [treeResponse, roleResponse] = await Promise.all([
      loadMenuTree(),
      organizationAPI.getRoleDetail(row.role_id)
    ])

    const roleMenus = roleResponse.data.menus?.map(m => m.menu_id) || []
    console.log('角色菜单ID列表:', roleMenus)

    // 等待DOM更新
    await nextTick()

    // 设置选中的菜单
    selectedMenus.value = roleMenus

    // 等待树组件完全渲染后设置选中状态
    setTimeout(() => {
      if (menuTreeRef.value) {
        menuTreeRef.value.setCheckedKeys(roleMenus)
        console.log('菜单树自动勾选完成')
      }
    }, 100)

  } catch (error) {
    console.error('获取角色菜单失败:', error)
    ElMessage.error('获取角色菜单失败')
  }
}

const handleSubmit = async () => {
  try {
    await roleFormRef.value.validate()
    submitLoading.value = true

    if (isEdit.value) {
      await organizationAPI.updateRole(roleForm.role_id, roleForm)
      ElMessage.success('更新成功')
    } else {
      await organizationAPI.createRole(roleForm)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    loadRoleList()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

const handlePermissionSubmit = async () => {
  try {
    permissionSubmitLoading.value = true

    const checkedKeys = permissionTreeRef.value.getCheckedKeys()
    const halfCheckedKeys = permissionTreeRef.value.getHalfCheckedKeys()
    const allCheckedKeys = [...checkedKeys, ...halfCheckedKeys]

    // 过滤掉模块节点，只保留权限节点
    const permissionIds = allCheckedKeys.filter(key => !key.toString().startsWith('module_'))

    await organizationAPI.assignPermissions({
      role_id: currentRole.value.role_id,
      permission_ids: permissionIds
    })

    ElMessage.success('权限分配成功')
    permissionDialogVisible.value = false
    loadRoleList()
  } catch (error) {
    ElMessage.error('权限分配失败')
  } finally {
    permissionSubmitLoading.value = false
  }
}

const handleMenuSubmit = async () => {
  try {
    menuSubmitLoading.value = true

    const checkedKeys = menuTreeRef.value.getCheckedKeys()
    const halfCheckedKeys = menuTreeRef.value.getHalfCheckedKeys()
    const allCheckedKeys = [...checkedKeys, ...halfCheckedKeys]

    await organizationAPI.assignMenus({
      role_id: currentRole.value.role_id,
      menu_ids: allCheckedKeys
    })

    ElMessage.success('菜单分配成功')
    menuDialogVisible.value = false
    loadRoleList()
    // 刷新全局菜单
    menuStore.refreshMenus()
  } catch (error) {
    ElMessage.error('菜单分配失败')
  } finally {
    menuSubmitLoading.value = false
  }
}

const handleDialogClose = () => {
  resetRoleForm()
  roleFormRef.value?.clearValidate()
}

const resetRoleForm = () => {
  Object.assign(roleForm, {
    role_id: '',
    role_name: '',
    description: '',
    is_default: false,
    is_active: true
  })
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(() => {
  loadRoleList()
})
</script>

<style scoped>
.admin-roles {
  padding: 0;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  padding: 32px 24px;
  margin: -24px -24px 24px -24px;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="header-grid" width="40" height="40" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="40" height="40" fill="none"/><circle cx="20" cy="20" r="1" fill="rgba(255,255,255,0.1)"/><line x1="0" y1="20" x2="40" y2="20" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"/><line x1="20" y1="0" x2="20" y2="40" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23header-grid)"/></svg>');
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: white;
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.8);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.primary-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.primary-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 搜索卡片 */
.search-card {
  margin-bottom: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.search-form {
  margin: 0;
}

.search-input {
  width: 280px;
}

.search-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  font-weight: 600;
}

.reset-btn {
  border: 1px solid #d1d5db;
  color: #6b7280;
}

.reset-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

/* 数据卡片 */
.data-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: #3b82f6;
  font-size: 20px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.count-tag {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.table-container {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.permission-assignment,
.menu-assignment {
  padding: 20px 0;
}

.role-info {
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 8px;
  font-weight: 500;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.permission-tree,
.menu-tree {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  padding: 12px;
  background: #fafbfc;
}

.tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 8px;
}

.menu-name {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
  flex: 1;
}

.node-description {
  font-size: 12px;
  color: #6b7280;
}

.node-path {
  font-size: 12px;
  color: #3b82f6;
  font-family: monospace;
  flex-shrink: 0;
}

/* 表格样式 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  color: #374151;
  font-weight: 600;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

:deep(.el-table td) {
  border-bottom: 1px solid rgba(59, 130, 246, 0.05);
}

:deep(.el-table tr:hover td) {
  background: rgba(59, 130, 246, 0.02);
}

/* 状态标签 */
:deep(.el-tag) {
  border-radius: 6px;
  font-weight: 500;
}

/* 按钮样式 */
:deep(.el-button--primary) {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  font-weight: 600;
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
}

:deep(.el-button--danger) {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
}

/* 分页样式 */
:deep(.el-pagination) {
  margin-top: 24px;
  justify-content: center;
}

:deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  border-radius: 6px;
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px 12px 0 0;
  padding: 20px 24px;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

/* 树形控件样式 */
:deep(.el-tree) {
  background: transparent;
}

:deep(.el-tree-node__content) {
  border-radius: 6px;
  margin: 2px 0;
  transition: all 0.3s ease;
  padding: 8px 12px;
}

:deep(.el-tree-node__content:hover) {
  background: rgba(59, 130, 246, 0.08);
}

:deep(.el-tree-node.is-checked > .el-tree-node__content) {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

/* 菜单树特定样式 */
.menu-tree :deep(.el-tree-node__content) {
  min-height: 36px;
}

.menu-tree .tree-node {
  padding: 4px 0;
}

.menu-tree .menu-name {
  margin-left: 0;
  text-align: left;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.action-btn {
  min-width: 60px;
  font-weight: 600;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: none;
}

.edit-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
}

.edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.permission-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.permission-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.menu-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.menu-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3);
}

.delete-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.delete-btn:hover:not(.disabled-btn) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.disabled-btn {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%) !important;
  color: #d1d5db !important;
  cursor: not-allowed !important;
  opacity: 0.6;
}

.disabled-btn:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* 确保按钮在小屏幕上也能正常显示 */
@media (max-width: 1400px) {
  .action-buttons {
    flex-direction: column;
    gap: 4px;
    align-items: stretch;
  }

  .action-btn {
    min-width: 50px;
    font-size: 12px;
    padding: 4px 8px;
  }
}

/* 表格行悬停效果增强 */
:deep(.el-table tbody tr:hover .action-btn:not(.disabled-btn)) {
  transform: translateY(-1px);
}
</style>
