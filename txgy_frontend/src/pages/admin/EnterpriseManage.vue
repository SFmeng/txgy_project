<template>
  <div class="enterprise-manage-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">企业管理</h1>
          <p class="page-subtitle">管理平台上的企业信息和业务数据</p>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <div class="stat-number">{{ statistics.total || 0 }}</div>
            <div class="stat-label">总企业数</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ statistics.verified || 0 }}</div>
            <div class="stat-label">已认证</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ statistics.active || 0 }}</div>
            <div class="stat-label">活跃企业</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card class="search-card">
        <el-form :model="searchForm" inline class="search-form">
          <el-form-item label="企业名称">
            <el-input
              v-model="searchForm.company_name"
              placeholder="请输入企业名称"
              clearable
              class="search-input"
              prefix-icon="Search"
            />
          </el-form-item>
          <el-form-item label="企业类型">
            <el-select
              v-model="searchForm.company_type"
              placeholder="请选择企业类型"
              clearable
              class="search-select"
            >
              <el-option label="生产制造企业" value="manufacturer" />
              <el-option label="施工安装企业" value="constructor" />
              <el-option label="工程甲方企业" value="owner" />
              <el-option label="供应商企业" value="supplier" />
            </el-select>
          </el-form-item>
          <el-form-item label="认证状态">
            <el-select
              v-model="searchForm.verify_status"
              placeholder="请选择认证状态"
              clearable
              class="search-select"
            >
              <el-option label="已认证" value="verified" />
              <el-option label="未认证" value="unverified" />
              <el-option label="认证中" value="pending" />
            </el-select>
          </el-form-item>
          <el-form-item label="企业状态">
            <el-select
              v-model="searchForm.status"
              placeholder="请选择企业状态"
              clearable
              class="search-select"
            >
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
              <el-option label="冻结" value="frozen" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="handleSearch" class="search-btn">
              搜索
            </el-button>
            <el-button :icon="Refresh" @click="handleReset" class="reset-btn">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <el-card class="data-card">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon class="header-icon"><OfficeBuilding /></el-icon>
              <span class="header-title">企业列表</span>
              <el-tag type="info" class="count-tag">共 {{ pagination.total }} 家企业</el-tag>
            </div>
            <div class="header-actions">
              <el-button type="primary" :icon="Plus" @click="handleAdd" class="add-btn">
                新增企业
              </el-button>
              <el-button
                type="success"
                :icon="Check"
                @click="handleBatchEnable"
                :disabled="selectedEnterprises.length === 0"
                class="batch-enable-btn"
              >
                批量启用 ({{ selectedEnterprises.length }})
              </el-button>
              <el-button
                type="warning"
                :icon="Lock"
                @click="handleBatchDisable"
                :disabled="selectedEnterprises.length === 0"
                class="batch-disable-btn"
              >
                批量禁用 ({{ selectedEnterprises.length }})
              </el-button>
            </div>
          </div>
        </template>

        <div class="table-container" v-loading="loading">
          <el-table
            :data="enterpriseList"
            @selection-change="handleSelectionChange"
            stripe
            style="width: 100%"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="company_name" label="企业名称" min-width="200">
              <template #default="{ row }">
                <div class="company-info">
                  <div class="company-name">{{ row.company_name }}</div>
                  <div class="company-code">{{ row.company_code || '暂无编码' }}</div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="company_type" label="企业类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getCompanyTypeTagType(row.company_type)" size="small">
                  {{ getCompanyTypeText(row.company_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="verify_status" label="认证状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getVerifyStatusTagType(row.verify_status)" size="small">
                  {{ getVerifyStatusText(row.verify_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="contact_person" label="联系人" width="120" />
            <el-table-column prop="contact_phone" label="联系电话" width="140" />
            <el-table-column prop="address" label="企业地址" min-width="200" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
                  {{ row.status === 'active' ? '正常' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" :icon="View" @click="handleView(row)">
                  查看
                </el-button>
                <el-button type="success" size="small" :icon="Edit" @click="handleEdit(row)">
                  编辑
                </el-button>
                <el-button
                  :type="row.status === 'active' ? 'warning' : 'success'"
                  size="small"
                  :icon="row.status === 'active' ? Lock : Unlock"
                  @click="handleToggleStatus(row)"
                >
                  {{ row.status === 'active' ? '禁用' : '启用' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.size"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 企业详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="企业详情"
      width="800px"
      :close-on-click-modal="false"
    >
      <div class="enterprise-detail" v-if="currentEnterprise">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="企业名称">
            {{ currentEnterprise.company_name }}
          </el-descriptions-item>
          <el-descriptions-item label="企业编码">
            {{ currentEnterprise.company_code || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="企业类型">
            <el-tag :type="getCompanyTypeTagType(currentEnterprise.company_type)" size="small">
              {{ getCompanyTypeText(currentEnterprise.company_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="认证状态">
            <el-tag :type="getVerifyStatusTagType(currentEnterprise.verify_status)" size="small">
              {{ getVerifyStatusText(currentEnterprise.verify_status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="联系人">
            {{ currentEnterprise.contact_person }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ currentEnterprise.contact_phone }}
          </el-descriptions-item>
          <el-descriptions-item label="企业邮箱" span="2">
            {{ currentEnterprise.email || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="企业地址" span="2">
            {{ currentEnterprise.address }}
          </el-descriptions-item>
          <el-descriptions-item label="企业简介" span="2">
            {{ currentEnterprise.description || '暂无简介' }}
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">
            {{ formatDate(currentEnterprise.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="最后更新">
            {{ formatDate(currentEnterprise.updated_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEdit(currentEnterprise)">编辑企业</el-button>
      </template>
    </el-dialog>

    <!-- 企业编辑对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="isEditing ? '编辑企业' : '新增企业'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        :model="enterpriseForm"
        :rules="enterpriseRules"
        ref="enterpriseFormRef"
        label-width="100px"
      >
        <el-form-item label="企业名称" prop="company_name">
          <el-input v-model="enterpriseForm.company_name" placeholder="请输入企业名称" />
        </el-form-item>
        <el-form-item label="企业编码" prop="company_code">
          <el-input v-model="enterpriseForm.company_code" placeholder="请输入企业编码" />
        </el-form-item>
        <el-form-item label="企业类型" prop="company_type">
          <el-select v-model="enterpriseForm.company_type" placeholder="请选择企业类型" style="width: 100%">
            <el-option label="生产制造企业" value="manufacturer" />
            <el-option label="施工安装企业" value="constructor" />
            <el-option label="工程甲方企业" value="owner" />
            <el-option label="供应商企业" value="supplier" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="enterpriseForm.contact_person" placeholder="请输入联系人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="enterpriseForm.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="企业邮箱" prop="email">
          <el-input v-model="enterpriseForm.email" placeholder="请输入企业邮箱" />
        </el-form-item>
        <el-form-item label="企业地址" prop="address">
          <el-input
            v-model="enterpriseForm.address"
            type="textarea"
            :rows="2"
            placeholder="请输入企业地址"
          />
        </el-form-item>
        <el-form-item label="企业简介" prop="description">
          <el-input
            v-model="enterpriseForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入企业简介"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">
          {{ isEditing ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, View, Edit, Plus, Check, Lock, Unlock, OfficeBuilding
} from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const enterpriseList = ref([])
const selectedEnterprises = ref([])
const detailDialogVisible = ref(false)
const editDialogVisible = ref(false)
const isEditing = ref(false)
const currentEnterprise = ref(null)

// 统计数据
const statistics = ref({
  total: 0,
  verified: 0,
  active: 0
})

// 搜索表单
const searchForm = reactive({
  company_name: '',
  company_type: '',
  verify_status: '',
  status: ''
})

// 分页数据
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 企业表单
const enterpriseForm = reactive({
  company_name: '',
  company_code: '',
  company_type: '',
  contact_person: '',
  contact_phone: '',
  email: '',
  address: '',
  description: ''
})

// 表单引用
const enterpriseFormRef = ref()

// 表单验证规则
const enterpriseRules = {
  company_name: [
    { required: true, message: '请输入企业名称', trigger: 'blur' }
  ],
  company_type: [
    { required: true, message: '请选择企业类型', trigger: 'change' }
  ],
  contact_person: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 模拟数据
const mockEnterpriseList = [
  {
    id: 1,
    company_name: '华润防腐材料有限公司',
    company_code: 'HR001',
    company_type: 'manufacturer',
    verify_status: 'verified',
    contact_person: '张经理',
    contact_phone: '13800138001',
    email: 'hr@example.com',
    address: '北京市朝阳区建国路88号',
    description: '专业从事防腐材料生产制造',
    status: 'active',
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-20T15:45:00Z'
  },
  {
    id: 2,
    company_name: '中建保温工程有限公司',
    company_code: 'ZJ002',
    company_type: 'constructor',
    verify_status: 'verified',
    contact_person: '李工',
    contact_phone: '13900139002',
    email: 'zj@example.com',
    address: '上海市浦东新区世纪大道123号',
    description: '专业保温工程施工企业',
    status: 'active',
    created_at: '2024-01-10T09:20:00Z',
    updated_at: '2024-01-18T14:30:00Z'
  },
  {
    id: 3,
    company_name: '绿城地产开发有限公司',
    company_code: 'LC003',
    company_type: 'owner',
    verify_status: 'pending',
    contact_person: '王总',
    contact_phone: '13700137003',
    email: 'lc@example.com',
    address: '杭州市西湖区文三路456号',
    description: '房地产开发企业',
    status: 'active',
    created_at: '2024-01-20T11:15:00Z',
    updated_at: '2024-01-22T16:20:00Z'
  }
]

// 获取企业类型文本
const getCompanyTypeText = (type) => {
  const typeMap = {
    'manufacturer': '制造企业',
    'constructor': '施工企业',
    'owner': '甲方企业',
    'supplier': '供应商'
  }
  return typeMap[type] || '未知'
}

// 获取企业类型标签类型
const getCompanyTypeTagType = (type) => {
  const typeMap = {
    'manufacturer': 'primary',
    'constructor': 'success',
    'owner': 'warning',
    'supplier': 'info'
  }
  return typeMap[type] || ''
}

// 获取认证状态文本
const getVerifyStatusText = (status) => {
  const statusMap = {
    'verified': '已认证',
    'pending': '认证中',
    'unverified': '未认证'
  }
  return statusMap[status] || '未知'
}

// 获取认证状态标签类型
const getVerifyStatusTagType = (status) => {
  const statusMap = {
    'verified': 'success',
    'pending': 'warning',
    'unverified': 'info'
  }
  return statusMap[status] || ''
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 加载企业列表
const loadEnterpriseList = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 使用模拟数据
    enterpriseList.value = mockEnterpriseList
    pagination.total = mockEnterpriseList.length
    
    // 计算统计数据
    const total = enterpriseList.value.length
    const verified = enterpriseList.value.filter(item => item.verify_status === 'verified').length
    const active = enterpriseList.value.filter(item => item.status === 'active').length
    
    statistics.value = { total, verified, active }
    
    console.log('企业列表加载成功')
  } catch (error) {
    ElMessage.error('加载企业列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  console.log('搜索条件:', searchForm)
  loadEnterpriseList()
}

// 重置
const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  loadEnterpriseList()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedEnterprises.value = selection
}

// 查看详情
const handleView = (row) => {
  currentEnterprise.value = row
  detailDialogVisible.value = true
}

// 编辑企业
const handleEdit = (row) => {
  isEditing.value = !!row
  if (row) {
    Object.keys(enterpriseForm).forEach(key => {
      enterpriseForm[key] = row[key] || ''
    })
    currentEnterprise.value = row
  } else {
    Object.keys(enterpriseForm).forEach(key => {
      enterpriseForm[key] = ''
    })
    currentEnterprise.value = null
  }
  detailDialogVisible.value = false
  editDialogVisible.value = true
}

// 新增企业
const handleAdd = () => {
  handleEdit(null)
}

// 保存企业
const handleSave = async () => {
  if (!enterpriseFormRef.value) return
  
  try {
    await enterpriseFormRef.value.validate()
    saving.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(isEditing.value ? '企业信息更新成功' : '企业创建成功')
    editDialogVisible.value = false
    await loadEnterpriseList()
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error(isEditing.value ? '更新失败' : '创建失败')
    }
  } finally {
    saving.value = false
  }
}

// 切换状态
const handleToggleStatus = async (row) => {
  const action = row.status === 'active' ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(
      `确定要${action}企业"${row.company_name}"吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    row.status = row.status === 'active' ? 'inactive' : 'active'
    ElMessage.success(`${action}成功`)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`${action}失败`)
    }
  }
}

// 批量启用
const handleBatchEnable = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要启用选中的 ${selectedEnterprises.value.length} 家企业吗？`,
      '批量启用',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    selectedEnterprises.value.forEach(enterprise => {
      enterprise.status = 'active'
    })
    
    ElMessage.success('批量启用成功')
    selectedEnterprises.value = []
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量启用失败')
    }
  }
}

// 批量禁用
const handleBatchDisable = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要禁用选中的 ${selectedEnterprises.value.length} 家企业吗？`,
      '批量禁用',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    selectedEnterprises.value.forEach(enterprise => {
      enterprise.status = 'inactive'
    })
    
    ElMessage.success('批量禁用成功')
    selectedEnterprises.value = []
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量禁用失败')
    }
  }
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.size = size
  loadEnterpriseList()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.page = page
  loadEnterpriseList()
}

onMounted(() => {
  loadEnterpriseList()
})
</script>

<style scoped>
.enterprise-manage-page {
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

.header-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 80px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
  color: white;
}

.stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 24px;
}

.search-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.search-form {
  margin: 0;
}

.search-input, .search-select {
  width: 180px;
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

/* 表格区域 */
.table-section {
  margin-bottom: 24px;
}

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

.header-actions {
  display: flex;
  gap: 12px;
}

.add-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-enable-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-enable-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
}

.batch-disable-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-disable-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
}

.table-container {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 企业信息 */
.company-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.company-name {
  font-weight: 600;
  color: #1f2937;
}

.company-code {
  font-size: 12px;
  color: #6b7280;
  font-family: monospace;
}

/* 企业详情 */
.enterprise-detail {
  padding: 0;
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

/* 描述列表样式 */
:deep(.el-descriptions) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-descriptions__header) {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

:deep(.el-descriptions__body .el-descriptions__table) {
  border-radius: 8px;
}

/* 表单样式 */
:deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #3b82f6;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-textarea__inner) {
  border-radius: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    padding: 24px 16px;
    margin: -24px -24px 24px -24px;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .header-stats {
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;
  }

  .search-input, .search-select {
    width: 150px;
  }

  .header-actions {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
