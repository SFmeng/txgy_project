<template>
  <div class="admin-permissions">
    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="权限名称">
          <el-input v-model="searchForm.perm_name" placeholder="请输入权限名称" clearable />
        </el-form-item>
        <el-form-item label="所属模块">
          <el-select v-model="searchForm.module" placeholder="请选择模块" clearable>
            <el-option
              v-for="module in moduleList"
              :key="module"
              :label="module"
              :value="module"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="searchForm.action" placeholder="请选择操作类型" clearable>
            <el-option label="查看" value="view" />
            <el-option label="创建" value="create" />
            <el-option label="编辑" value="edit" />
            <el-option label="删除" value="delete" />
            <el-option label="审核" value="audit" />
            <el-option label="导出" value="export" />
            <el-option label="导入" value="import" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 权限列表 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>权限管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增权限
            </el-button>
            <el-button type="success" @click="handleRefresh">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
          </div>
        </div>
      </template>

      <div class="permission-content">
        <!-- 表格展示 -->
        <div class="table-view">
          <el-table
            :data="permissionList"
            style="width: 100%"
            v-loading="loading"
            :header-cell-style="{ background: '#f8fafc', color: '#374151', fontWeight: '600' }"
            :row-style="{ height: '60px' }"
            stripe
            border
            empty-text="暂无权限数据"
          >
            <el-table-column type="index" label="#" width="60" align="center" />

            <el-table-column prop="perm_name" label="权限名称" width="180" show-overflow-tooltip>
              <template #default="scope">
                <div class="permission-name">
                  <el-icon class="permission-icon" :color="getPermissionIconColor(scope.row.action)">
                    <component :is="getPermissionIcon(scope.row.action)" />
                  </el-icon>
                  <span class="name-text">{{ scope.row.perm_name }}</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="perm_code" label="权限标识" width="220" show-overflow-tooltip>
              <template #default="scope">
                <el-tag class="code-tag" type="info" effect="plain">
                  {{ scope.row.perm_code }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column prop="module" label="所属模块" width="140">
              <template #default="scope">
                <el-tag class="module-tag" :color="getModuleColor(scope.row.module)" effect="light">
                  {{ scope.row.module }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column prop="function" label="所属功能" width="140" show-overflow-tooltip />

            <el-table-column prop="action" label="操作类型" width="120" align="center">
              <template #default="scope">
                <el-tag :type="getActionType(scope.row.action)" size="default" effect="dark">
                  {{ getActionText(scope.row.action) }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column prop="api_path" label="API接口" width="280" show-overflow-tooltip>
              <template #default="scope">
                <div class="api-info" v-if="scope.row.api_path">
                  <el-tag
                    :type="getMethodType(scope.row.api_method)"
                    size="small"
                    class="method-tag"
                    effect="dark"
                  >
                    {{ scope.row.api_method }}
                  </el-tag>
                  <code class="api-path">{{ scope.row.api_path }}</code>
                </div>
                <span v-else class="no-api">-</span>
              </template>
            </el-table-column>

            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
              <template #default="scope">
                <span class="description-text">{{ scope.row.description || '暂无描述' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="140" fixed="right" align="center">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button
                    size="small"
                    type="primary"
                    :icon="Edit"
                    circle
                    @click="handleEdit(scope.row)"
                    title="编辑权限"
                  />
                  <el-button
                    size="small"
                    type="danger"
                    :icon="Delete"
                    circle
                    @click="handleDelete(scope.row)"
                    title="删除权限"
                  />
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


      </div>
    </el-card>

    <!-- 权限编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="permissionFormRef"
        :model="permissionForm"
        :rules="permissionFormRules"
        label-width="100px"
      >
        <el-form-item label="权限名称" prop="perm_name">
          <el-input v-model="permissionForm.perm_name" />
        </el-form-item>
        <el-form-item label="权限标识" prop="perm_code">
          <el-input v-model="permissionForm.perm_code" placeholder="如: user.view" />
        </el-form-item>
        <el-form-item label="所属模块" prop="module">
          <el-input v-model="permissionForm.module" />
        </el-form-item>
        <el-form-item label="所属功能" prop="function">
          <el-input v-model="permissionForm.function" />
        </el-form-item>
        <el-form-item label="操作类型" prop="action">
          <el-select v-model="permissionForm.action" style="width: 100%">
            <el-option label="查看" value="view" />
            <el-option label="创建" value="create" />
            <el-option label="编辑" value="edit" />
            <el-option label="删除" value="delete" />
            <el-option label="审核" value="audit" />
            <el-option label="导出" value="export" />
            <el-option label="导入" value="import" />
          </el-select>
        </el-form-item>
        <el-form-item label="API路径" prop="api_path">
          <el-input v-model="permissionForm.api_path" placeholder="如: /api/v1/users/" />
        </el-form-item>
        <el-form-item label="API方法" prop="api_method">
          <el-select v-model="permissionForm.api_method" style="width: 100%">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
            <el-option label="PATCH" value="PATCH" />
          </el-select>
        </el-form-item>
        <el-form-item label="权限描述" prop="description">
          <el-input v-model="permissionForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, Edit, Delete, View, Lock, Setting,
  Document, Upload, Download, Check, Close
} from '@element-plus/icons-vue'
import { organizationAPI } from '@/api/organization'

// 响应式数据
const loading = ref(false)
const permissionList = ref([])
const moduleList = ref([])

// 搜索表单
const searchForm = reactive({
  perm_name: '',
  module: '',
  action: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 权限编辑对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const submitLoading = ref(false)
const permissionFormRef = ref()
const permissionTreeRef = ref()

const permissionForm = reactive({
  perm_id: '',
  perm_name: '',
  perm_code: '',
  module: '',
  function: '',
  action: 'view',
  api_path: '',
  api_method: 'GET',
  description: ''
})

const permissionFormRules = {
  perm_name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' }
  ],
  perm_code: [
    { required: true, message: '请输入权限标识', trigger: 'blur' },
    { pattern: /^[a-z_]+\.[a-z_]+$/, message: '权限标识格式为: module.action', trigger: 'blur' }
  ],
  module: [
    { required: true, message: '请输入所属模块', trigger: 'blur' }
  ],
  function: [
    { required: true, message: '请输入所属功能', trigger: 'blur' }
  ],
  action: [
    { required: true, message: '请选择操作类型', trigger: 'change' }
  ]
}



// 方法
const loadPermissions = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }

    const response = await organizationAPI.getPermissions(params)
    permissionList.value = response.data.results || response.data || []
    pagination.total = response.data.total || permissionList.value.length

    // 提取模块列表
    const modules = [...new Set(permissionList.value.map(p => p.module).filter(Boolean))]
    moduleList.value = modules
  } catch (error) {
    ElMessage.error('加载权限列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadPermissions()
}

const handleReset = () => {
  Object.assign(searchForm, {
    perm_name: '',
    module: '',
    action: ''
  })
  pagination.page = 1
  loadPermissions()
}

const handleRefresh = () => {
  loadPermissions()
}

// 获取权限图标
const getPermissionIcon = (action) => {
  const iconMap = {
    view: View,
    create: Plus,
    edit: Edit,
    delete: Delete,
    audit: Check,
    export: Download,
    import: Upload,
    manage: Setting
  }
  return iconMap[action] || Lock
}

// 获取权限图标颜色
const getPermissionIconColor = (action) => {
  const colorMap = {
    view: '#409eff',
    create: '#67c23a',
    edit: '#e6a23c',
    delete: '#f56c6c',
    audit: '#909399',
    export: '#409eff',
    import: '#67c23a',
    manage: '#e6a23c'
  }
  return colorMap[action] || '#909399'
}

// 获取模块颜色
const getModuleColor = (module) => {
  const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#c71585', '#ff8c00', '#32cd32']
  const hash = module ? module.split('').reduce((a, b) => a + b.charCodeAt(0), 0) : 0
  return colors[hash % colors.length]
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadPermissions()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadPermissions()
}

const handleAdd = () => {
  dialogTitle.value = '新增权限'
  isEdit.value = false
  dialogVisible.value = true
  resetPermissionForm()
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑权限'
  isEdit.value = true
  dialogVisible.value = true

  Object.assign(permissionForm, {
    perm_id: row.perm_id,
    perm_name: row.perm_name,
    perm_code: row.perm_code,
    module: row.module,
    function: row.function,
    action: row.action,
    api_path: row.api_path,
    api_method: row.api_method,
    description: row.description
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除权限 "${row.perm_name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await organizationAPI.deletePermission(row.perm_id)
    ElMessage.success('删除成功')
    loadPermissions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  try {
    await permissionFormRef.value.validate()
    submitLoading.value = true

    if (isEdit.value) {
      await organizationAPI.updatePermission(permissionForm.perm_id, permissionForm)
      ElMessage.success('更新成功')
    } else {
      await organizationAPI.createPermission(permissionForm)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    loadPermissions()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDialogClose = () => {
  resetPermissionForm()
  permissionFormRef.value?.clearValidate()
}

const resetPermissionForm = () => {
  Object.assign(permissionForm, {
    perm_id: '',
    perm_name: '',
    perm_code: '',
    module: '',
    function: '',
    action: 'view',
    api_path: '',
    api_method: 'GET',
    description: ''
  })
}

// 工具方法
const getActionType = (action) => {
  const typeMap = {
    view: 'info',
    create: 'success',
    edit: 'warning',
    delete: 'danger',
    audit: 'primary',
    export: 'success',
    import: 'warning'
  }
  return typeMap[action] || 'info'
}

const getActionText = (action) => {
  const textMap = {
    view: '查看',
    create: '创建',
    edit: '编辑',
    delete: '删除',
    audit: '审核',
    export: '导出',
    import: '导入'
  }
  return textMap[action] || action
}

const getMethodType = (method) => {
  const typeMap = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger',
    PATCH: 'info'
  }
  return typeMap[method] || 'info'
}

onMounted(() => {
  loadPermissions()
})
</script>

<style scoped>
.admin-permissions {
  padding: 0;
  background: #f5f7fa;
  min-height: 100vh;
}

.search-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: none;
}

.search-card :deep(.el-card__body) {
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button {
  border-radius: 8px;
  font-weight: 500;
}

.permission-content {
  position: relative;
  margin-top: 20px;
}

.permission-content .el-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: none;
}

.permission-content :deep(.el-card__body) {
  padding: 24px;
}

.table-view {
  min-height: 400px;
}

.table-view :deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

.table-view :deep(.el-table__header-wrapper) {
  border-radius: 8px 8px 0 0;
}

.table-view :deep(.el-table__body-wrapper) {
  border-radius: 0 0 8px 8px;
}

.table-view :deep(.el-table th) {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 2px solid #e2e8f0;
}

.table-view :deep(.el-table td) {
  border-bottom: 1px solid #f1f5f9;
}

.table-view :deep(.el-table__row:hover) {
  background-color: #f8fafc;
}

.table-view :deep(.el-table__row:hover td) {
  background-color: transparent;
}

/* 权限名称样式 */
.permission-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.permission-icon {
  font-size: 16px;
}

.name-text {
  font-weight: 500;
  color: #303133;
}

/* 权限标识样式 */
.code-tag {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  border: 1px solid #d9ecff;
  background-color: #ecf5ff;
  color: #409eff;
}

/* 模块标签样式 */
.module-tag {
  font-weight: 500;
  border: none;
}

/* API信息样式 */
.api-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.method-tag {
  font-weight: 600;
  min-width: 50px;
  text-align: center;
}

.api-path {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #606266;
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid #e4e7ed;
}

.no-api {
  color: #c0c4cc;
  font-style: italic;
}

/* 描述文本样式 */
.description-text {
  color: #606266;
  line-height: 1.4;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}




</style>
