<template>
  <div class="admin-users">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">用户管理</h1>
          <p class="page-subtitle">管理系统用户信息，分配角色权限</p>
        </div>
        <div class="header-actions">
          <el-button type="warning" @click="$router.push('/admin/enterprise')" class="enterprise-btn">
            <el-icon><OfficeBuilding /></el-icon>
            企业认证
          </el-button>
          <el-button type="primary" @click="handleAdd" class="primary-btn">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索和操作栏 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="用户名">
          <el-input
            v-model="searchForm.username"
            placeholder="请输入用户名"
            clearable
            class="search-input"
            prefix-icon="Search"
          />
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="searchForm.user_type" placeholder="请选择用户类型" clearable class="search-select">
            <el-option label="企业用户" value="enterprise" />
            <el-option label="个人用户" value="individual" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable class="search-select">
            <el-option label="激活" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
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

    <!-- 用户列表 -->
    <el-card class="data-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><UserFilled /></el-icon>
            <span class="header-title">用户列表</span>
            <el-tag type="info" class="count-tag">共 {{ pagination.total }} 个用户</el-tag>
          </div>
          <div class="header-actions">
            <el-button
              type="success"
              @click="handleBatchAssignRoles"
              :disabled="!selectedUsers.length"
              class="batch-btn"
            >
              <el-icon><UserFilled /></el-icon>
              批量分配角色 ({{ selectedUsers.length }})
            </el-button>
          </div>
        </div>
      </template>

      <div class="table-container">
        <el-table
          :data="userList"
          style="width: 100%"
          v-loading="loading"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="user_id" label="用户ID" width="120" />
          <el-table-column prop="username" label="用户名" width="120" />
          <el-table-column prop="real_name" label="真实姓名" width="120" />
          <el-table-column prop="email" label="邮箱" width="180" />
          <el-table-column prop="phone" label="手机号" width="120" />
          <el-table-column prop="user_type" label="用户类型" width="100">
            <template #default="scope">
              <el-tag :type="getUserTypeTag(scope.row.user_type)">
                {{ getUserTypeText(scope.row.user_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="role_names" label="角色" width="200">
            <template #default="scope">
              <el-tag
                v-for="role in scope.row.role_names"
                :key="role"
                size="small"
                style="margin-right: 4px;"
              >
                {{ role }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="80">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                {{ scope.row.status === 'active' ? '激活' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="date_joined" label="注册时间" width="160">
            <template #default="scope">
              {{ formatDate(scope.row.date_joined) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="320" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="handleView(scope.row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" @click="handleEdit(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="warning" @click="handleAssignRoles(scope.row)">
                <el-icon><UserFilled /></el-icon>
                角色
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
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

    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userFormRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="userForm.real_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userForm.phone" />
        </el-form-item>
        <el-form-item label="用户类型" prop="user_type">
          <el-select v-model="userForm.user_type" style="width: 100%">
            <el-option label="企业用户" value="enterprise" />
            <el-option label="个人用户" value="individual" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="userForm.status" style="width: 100%">
            <el-option label="激活" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="确认密码" prop="password_confirm">
          <el-input v-model="userForm.password_confirm" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 角色分配对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      :title="currentUser ? '分配角色' : '批量分配角色'"
      width="500px"
    >
      <div class="role-assignment">
        <div class="user-info">
          <span v-if="currentUser">
            用户：{{ currentUser.real_name || currentUser.username }}
          </span>
          <span v-else>
            批量分配角色给 {{ selectedUsers.length }} 个用户
          </span>
        </div>
        <el-checkbox-group v-model="selectedRoles">
          <el-checkbox
            v-for="role in roleList"
            :key="role.role_id"
            :label="role.role_id"
            :disabled="!role.is_active"
          >
            {{ role.role_name }}
            <span class="role-desc">{{ role.description }}</span>
          </el-checkbox>
        </el-checkbox-group>
      </div>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRoleSubmit" :loading="roleSubmitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 用户详情对话框 -->
    <UserDetailDialog
      v-model="userDetailVisible"
      :user-info="currentViewUser"
      @edit="handleEditFromDetail"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, Edit, Delete, UserFilled, OfficeBuilding, View
} from '@element-plus/icons-vue'
import { authAPI } from '@/api/auth'
import { organizationAPI } from '@/api/organization'
import UserDetailDialog from '@/components/UserDetailDialog.vue'

// 响应式数据
const loading = ref(false)
const userList = ref([])
const selectedUsers = ref([])
const roleList = ref([])

// 搜索表单
const searchForm = reactive({
  username: '',
  user_type: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 用户编辑对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const submitLoading = ref(false)
const userFormRef = ref()

// 用户详情对话框
const userDetailVisible = ref(false)
const currentViewUser = ref({})

const userForm = reactive({
  user_id: '',
  username: '',
  real_name: '',
  email: '',
  phone: '',
  user_type: 'enterprise',
  status: 'active',
  password: '',
  password_confirm: ''
})

const userFormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  user_type: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== userForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 角色分配对话框
const roleDialogVisible = ref(false)
const currentUser = ref(null)
const selectedRoles = ref([])
const roleSubmitLoading = ref(false)

// 方法
const loadUserList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }

    const response = await authAPI.getUserList(params)
    userList.value = response.data.results || []
    pagination.total = response.data.total || 0
  } catch (error) {
    ElMessage.error('加载用户列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadRoleList = async () => {
  try {
    const response = await organizationAPI.getRoles()
    roleList.value = response.data.results || []
  } catch (error) {
    console.error('加载角色列表失败:', error)
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadUserList()
}

const handleReset = () => {
  Object.assign(searchForm, {
    username: '',
    user_type: '',
    status: ''
  })
  pagination.page = 1
  loadUserList()
}

const handleSelectionChange = (selection) => {
  selectedUsers.value = selection
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadUserList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadUserList()
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  isEdit.value = false
  dialogVisible.value = true
  resetUserForm()
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  isEdit.value = true
  dialogVisible.value = true

  nextTick(() => {
    Object.assign(userForm, {
      user_id: row.user_id,
      username: row.username,
      real_name: row.real_name,
      email: row.email,
      phone: row.phone,
      user_type: row.user_type,
      status: row.status,
      password: ''
    })
  })
}

const handleView = (row) => {
  // 打开用户详情对话框
  currentViewUser.value = { ...row }
  userDetailVisible.value = true
}

// 从用户详情对话框编辑用户
const handleEditFromDetail = (userInfo) => {
  handleEdit(userInfo)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.real_name || row.username}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await authAPI.deleteUser(row.user_id)
    ElMessage.success('删除成功')
    loadUserList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleAssignRoles = async (row) => {
  currentUser.value = row
  roleDialogVisible.value = true

  // 获取用户当前角色
  selectedRoles.value = row.roles?.map(role => role.role_id) || []
}

const handleBatchAssignRoles = () => {
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请选择要分配角色的用户')
    return
  }

  // 设置批量分配模式
  currentUser.value = null
  selectedRoles.value = []
  roleDialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await userFormRef.value.validate()
    submitLoading.value = true

    if (isEdit.value) {
      await authAPI.updateUser(userForm.user_id, userForm)
      ElMessage.success('更新成功')
    } else {
      await authAPI.createUser(userForm)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    loadUserList()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

const handleRoleSubmit = async () => {
  try {
    roleSubmitLoading.value = true

    // 确定要分配角色的用户ID列表
    const userIds = currentUser.value
      ? [currentUser.value.user_id]
      : selectedUsers.value.map(user => user.user_id)

    await organizationAPI.assignRoles({
      user_ids: userIds,
      role_ids: selectedRoles.value
    })

    const message = currentUser.value ? '角色分配成功' : `批量分配角色成功，共 ${userIds.length} 个用户`
    ElMessage.success(message)
    roleDialogVisible.value = false
    selectedUsers.value = [] // 清空选中的用户
    loadUserList()
  } catch (error) {
    ElMessage.error('角色分配失败')
  } finally {
    roleSubmitLoading.value = false
  }
}

const handleDialogClose = () => {
  resetUserForm()
  userFormRef.value?.clearValidate()
}

const resetUserForm = () => {
  Object.assign(userForm, {
    user_id: '',
    username: '',
    real_name: '',
    email: '',
    phone: '',
    user_type: 'enterprise',
    status: 'active',
    password: '',
    password_confirm: ''
  })
}

// 工具方法
const getUserTypeTag = (type) => {
  const typeMap = {
    enterprise: 'primary',
    individual: 'success',
    admin: 'danger'
  }
  return typeMap[type] || 'info'
}

const getUserTypeText = (type) => {
  const typeMap = {
    enterprise: '企业用户',
    individual: '个人用户',
    admin: '管理员'
  }
  return typeMap[type] || '未知'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 企业类型文本映射
const getCompanyTypeText = (type) => {
  const typeMap = {
    manufacturer: '生产制造企业',
    constructor: '施工安装企业',
    owner: '工程甲方企业',
    supplier: '供应商企业',
    unknown: '未知'
  }
  return typeMap[type] || '未知'
}

// 认证状态文本映射
const getVerifyStatusText = (status) => {
  const statusMap = {
    pending: '待审核',
    verified: '已通过',
    rejected: '已拒绝'
  }
  return statusMap[status] || '未知'
}

// 认证状态颜色映射
const getVerifyStatusColor = (status) => {
  const colorMap = {
    pending: '#E6A23C',
    verified: '#67C23A',
    rejected: '#F56C6C'
  }
  return colorMap[status] || '#909399'
}

onMounted(() => {
  loadUserList()
  loadRoleList()
})
</script>

<style scoped>
.admin-users {
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

.primary-btn, .enterprise-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.primary-btn:hover, .enterprise-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.enterprise-btn {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.3);
}

.enterprise-btn:hover {
  background: rgba(245, 158, 11, 0.3);
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

.search-input, .search-select {
  width: 200px;
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

.batch-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
}

.table-container {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.role-assignment {
  padding: 20px 0;
}

.user-info {
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 8px;
  font-weight: 500;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.role-desc {
  font-size: 12px;
  color: #6b7280;
  margin-left: 8px;
}

.el-checkbox {
  display: block;
  margin-bottom: 12px;
  margin-right: 0;
}

.el-checkbox__label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
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

/* 复选框样式 */
:deep(.el-checkbox) {
  border-radius: 6px;
  padding: 8px 12px;
  margin: 4px 0;
  transition: all 0.3s ease;
}

:deep(.el-checkbox:hover) {
  background: rgba(59, 130, 246, 0.05);
}

:deep(.el-checkbox.is-checked) {
  background: rgba(59, 130, 246, 0.1);
}
</style>
