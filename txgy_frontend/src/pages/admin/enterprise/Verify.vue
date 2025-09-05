<template>
  <div class="enterprise-verify-page">
    <!-- 统计卡片 -->
    <el-card class="stats-card">
      <div class="stats-content">
        <div class="stats-header">
          <h2 class="stats-title">
            <el-icon><DocumentChecked /></el-icon>
            企业认证概览
          </h2>
        </div>
        <div class="stats-grid">
          <div class="stat-item pending">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.pending || 0 }}</div>
              <div class="stat-label">待审核</div>
            </div>
          </div>
          <div class="stat-item approved">
            <div class="stat-icon">
              <el-icon><SuccessFilled /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.approved || 0 }}</div>
              <div class="stat-label">已通过</div>
            </div>
          </div>
          <div class="stat-item rejected">
            <div class="stat-icon">
              <el-icon><CircleClose /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.rejected || 0 }}</div>
              <div class="stat-label">已拒绝</div>
            </div>
          </div>
          <div class="stat-item total">
            <div class="stat-icon">
              <el-icon><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.total || 0 }}</div>
              <div class="stat-label">总企业数</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

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
          <el-form-item label="认证状态">
            <el-select
              v-model="searchForm.verify_status"
              placeholder="请选择认证状态"
              clearable
              class="search-select"
            >
              <el-option label="待审核" value="pending" />
              <el-option label="已通过" value="verified" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
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
              <span class="header-title">企业认证列表</span>
              <el-tag type="info" class="count-tag">共 {{ pagination.total }} 家企业</el-tag>
            </div>
            <div class="header-actions">
              <el-button
                type="success"
                :icon="DocumentChecked"
                @click="handleBatchApprove"
                :disabled="selectedEnterprises.length === 0"
                class="batch-approve-btn"
              >
                批量通过 ({{ selectedEnterprises.length }})
              </el-button>
              <el-button
                type="danger"
                :icon="Close"
                @click="handleBatchReject"
                :disabled="selectedEnterprises.length === 0"
                class="batch-reject-btn"
              >
                批量拒绝 ({{ selectedEnterprises.length }})
              </el-button>
            </div>
          </div>
        </template>

        <div class="table-container">
          <el-table
            :data="enterpriseList"
            style="width: 100%"
            v-loading="loading"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="company_name" label="企业名称" width="200" />
            <el-table-column prop="company_type" label="企业类型" width="120">
              <template #default="scope">
                <el-tag :type="getCompanyTypeTag(scope.row.company_type)">
                  {{ getCompanyTypeText(scope.row.company_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="contact_person" label="联系人" width="100" />
            <el-table-column prop="contact_phone" label="联系电话" width="120" />
            <el-table-column prop="verify_status" label="认证状态" width="100">
              <template #default="scope">
                <el-tag :type="getVerifyStatusTag(scope.row.verify_status)">
                  {{ getVerifyStatusText(scope.row.verify_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="申请时间" width="160">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="verified_at" label="审核时间" width="160">
              <template #default="scope">
                {{ scope.row.verified_at ? formatDate(scope.row.verified_at) : '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="280" fixed="right">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button
                    type="primary"
                    size="small"
                    :icon="View"
                    @click="handleView(scope.row)"
                    class="action-btn view-btn"
                  >
                    查看
                  </el-button>
                  <el-button
                    v-if="scope.row.verify_status === 'pending'"
                    type="success"
                    size="small"
                    :icon="Check"
                    @click="handleApprove(scope.row)"
                    class="action-btn approve-btn"
                  >
                    通过
                  </el-button>
                  <el-button
                    v-if="scope.row.verify_status === 'pending'"
                    type="danger"
                    size="small"
                    :icon="Close"
                    @click="handleReject(scope.row)"
                    class="action-btn reject-btn"
                  >
                    拒绝
                  </el-button>
                  <div v-if="scope.row.verify_status !== 'pending'" class="status-info">
                    <el-tag
                      :type="scope.row.verify_status === 'verified' ? 'success' : 'danger'"
                      size="small"
                    >
                      {{ scope.row.verify_status === 'verified' ? '已通过' : '已拒绝' }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadEnterpriseList"
            @current-change="loadEnterpriseList"
          />
        </div>
      </el-card>
    </div>

    <!-- 企业详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="企业认证详情"
      width="800px"
    >
      <div v-if="currentEnterprise" class="enterprise-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="企业名称">
            {{ currentEnterprise.company_name }}
          </el-descriptions-item>
          <el-descriptions-item label="企业类型">
            <el-tag :type="getCompanyTypeTag(currentEnterprise.company_type)">
              {{ getCompanyTypeText(currentEnterprise.company_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="联系人">
            {{ currentEnterprise.contact_person }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ currentEnterprise.contact_phone }}
          </el-descriptions-item>
          <el-descriptions-item label="企业地址" span="2">
            {{ currentEnterprise.address }}
          </el-descriptions-item>
          <el-descriptions-item label="营业执照号">
            {{ currentEnterprise.business_license }}
          </el-descriptions-item>
          <el-descriptions-item label="认证状态">
            <el-tag :type="getVerifyStatusTag(currentEnterprise.verify_status)">
              {{ getVerifyStatusText(currentEnterprise.verify_status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请时间">
            {{ formatDate(currentEnterprise.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="审核时间">
            {{ currentEnterprise.verified_at ? formatDate(currentEnterprise.verified_at) : '未审核' }}
          </el-descriptions-item>
          <el-descriptions-item label="企业简介" span="2">
            {{ currentEnterprise.description || '暂无简介' }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 认证材料 -->
        <div class="verify-materials" v-if="currentEnterprise.materials">
          <h4>认证材料</h4>
          <div class="materials-grid">
            <div
              v-for="material in currentEnterprise.materials"
              :key="material.id"
              class="material-item"
            >
              <el-image
                :src="material.file_url"
                :preview-src-list="[material.file_url]"
                fit="cover"
                style="width: 100px; height: 100px"
              />
              <p>{{ material.file_name }}</p>
            </div>
          </div>
        </div>

        <!-- 审核操作 -->
        <div class="verify-actions" v-if="currentEnterprise.verify_status === 'pending'">
          <el-divider />
          <div class="action-buttons">
            <el-button
              type="success"
              :icon="Check"
              @click="handleApprove(currentEnterprise)"
            >
              通过认证
            </el-button>
            <el-button
              type="danger"
              :icon="Close"
              @click="handleReject(currentEnterprise)"
            >
              拒绝认证
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 审核备注对话框 -->
    <el-dialog
      v-model="remarkDialogVisible"
      :title="remarkDialogTitle"
      width="500px"
    >
      <el-form :model="remarkForm" label-width="80px">
        <el-form-item label="审核备注">
          <el-input
            v-model="remarkForm.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入审核备注（可选）"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="remarkDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="remarkSubmitLoading"
          @click="handleRemarkSubmit"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, View, Check, Close, DocumentChecked, OfficeBuilding, Clock, SuccessFilled, CircleClose
} from '@element-plus/icons-vue'
import { authAPI } from '@/api/auth'

// 响应式数据
const loading = ref(false)
const enterpriseList = ref([])
const selectedEnterprises = ref([])

// 统计数据
const statistics = ref({
  pending: 0,
  approved: 0,
  rejected: 0,
  total: 0
})

// 搜索表单
const searchForm = reactive({
  company_name: '',
  verify_status: '',
  company_type: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 详情对话框
const detailDialogVisible = ref(false)
const currentEnterprise = ref(null)

// 审核备注对话框
const remarkDialogVisible = ref(false)
const remarkDialogTitle = ref('')
const remarkForm = reactive({
  remark: ''
})
const remarkSubmitLoading = ref(false)
const currentVerifyAction = ref('')
const currentVerifyEnterprise = ref(null)

// 方法
const loadEnterpriseList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      user_type: 'enterprise',
      ...searchForm
    }

    const response = await authAPI.getUserList(params)
    
    // 过滤出企业用户并添加企业信息
    enterpriseList.value = response.data.results
      .filter(user => user.user_type === 'enterprise')
      .map(user => ({
        ...user,
        company_name: user.enterprise_info?.company_name || '未填写',
        company_type: user.enterprise_info?.company_type || 'unknown',
        contact_person: user.real_name || user.username,
        contact_phone: user.phone || '未填写',
        verify_status: user.enterprise_info?.certification_status || 'pending',
        verified_at: user.enterprise_info?.verified_at,
        address: user.enterprise_info?.address || '未填写',
        business_license: user.enterprise_info?.business_license || '未填写',
        description: user.enterprise_info?.description || '',
        materials: user.enterprise_info?.materials || []
      }))
    
    pagination.total = response.data.total || 0

    // 计算统计数据
    const pending = enterpriseList.value.filter(item => item.verify_status === 'pending').length
    const approved = enterpriseList.value.filter(item => item.verify_status === 'verified').length
    const rejected = enterpriseList.value.filter(item => item.verify_status === 'rejected').length

    statistics.value = {
      pending,
      approved,
      rejected,
      total: enterpriseList.value.length
    }
  } catch (error) {
    ElMessage.error('加载企业列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadEnterpriseList()
}

const handleReset = () => {
  Object.assign(searchForm, {
    company_name: '',
    verify_status: '',
    company_type: ''
  })
  pagination.page = 1
  loadEnterpriseList()
}

const handleSelectionChange = (selection) => {
  selectedEnterprises.value = selection
}

const handleView = (row) => {
  currentEnterprise.value = row
  detailDialogVisible.value = true
}

const handleApprove = (row) => {
  currentVerifyEnterprise.value = row
  currentVerifyAction.value = 'approve'
  remarkDialogTitle.value = '通过企业认证'
  remarkForm.remark = ''
  remarkDialogVisible.value = true
}

const handleReject = (row) => {
  currentVerifyEnterprise.value = row
  currentVerifyAction.value = 'reject'
  remarkDialogTitle.value = '拒绝企业认证'
  remarkForm.remark = ''
  remarkDialogVisible.value = true
}

const handleRemarkSubmit = async () => {
  try {
    remarkSubmitLoading.value = true
    
    const enterprise = currentVerifyEnterprise.value
    const action = currentVerifyAction.value
    
    // 调用企业认证API
    await authAPI.enterpriseVerify({
      user_id: enterprise.user_id,
      action: action,
      remark: remarkForm.remark
    })
    
    ElMessage.success(action === 'approve' ? '认证通过成功' : '认证拒绝成功')
    remarkDialogVisible.value = false
    loadEnterpriseList()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  } finally {
    remarkSubmitLoading.value = false
  }
}

const handleBatchApprove = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要批量通过 ${selectedEnterprises.value.length} 个企业的认证吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    for (const enterprise of selectedEnterprises.value) {
      if (enterprise.verify_status === 'pending') {
        await authAPI.enterpriseVerify({
          user_id: enterprise.user_id,
          action: 'approve',
          remark: '批量审核通过'
        })
      }
    }

    ElMessage.success('批量审核通过成功')
    loadEnterpriseList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量操作失败')
    }
  }
}

const handleBatchReject = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要批量拒绝 ${selectedEnterprises.value.length} 个企业的认证吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    for (const enterprise of selectedEnterprises.value) {
      if (enterprise.verify_status === 'pending') {
        await authAPI.enterpriseVerify({
          user_id: enterprise.user_id,
          action: 'reject',
          remark: '批量审核拒绝'
        })
      }
    }

    ElMessage.success('批量审核拒绝成功')
    loadEnterpriseList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量操作失败')
    }
  }
}

// 工具方法
const getCompanyTypeText = (type) => {
  const typeMap = {
    manufacturer: '生产制造',
    constructor: '施工安装',
    owner: '工程甲方',
    supplier: '供应商',
    unknown: '未知'
  }
  return typeMap[type] || '未知'
}

const getCompanyTypeTag = (type) => {
  const tagMap = {
    manufacturer: 'primary',
    constructor: 'success',
    owner: 'warning',
    supplier: 'info',
    unknown: 'info'
  }
  return tagMap[type] || 'info'
}

const getVerifyStatusText = (status) => {
  const statusMap = {
    pending: '待审核',
    verified: '已通过',
    rejected: '已拒绝'
  }
  return statusMap[status] || '未知'
}

const getVerifyStatusTag = (status) => {
  const tagMap = {
    pending: 'warning',
    verified: 'success',
    rejected: 'danger'
  }
  return tagMap[status] || 'info'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadEnterpriseList()
})
</script>

<style scoped>
.enterprise-verify-page {
  padding: 0;
}

/* 统计卡片 */
.stats-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stats-content {
  padding: 20px;
}

.stats-header {
  margin-bottom: 20px;
}

.stats-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-item.pending {
  background: linear-gradient(135deg, #fef7e0 0%, #fff7e6 100%);
  border-color: #e6a23c;
}

.stat-item.approved {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  border-color: #67c23a;
}

.stat-item.rejected {
  background: linear-gradient(135deg, #fef0f0 0%, #fdf2f2 100%);
  border-color: #f56c6c;
}

.stat-item.total {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  border-color: #409eff;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.stat-item.pending .stat-icon { background: #e6a23c; }
.stat-item.approved .stat-icon { background: #67c23a; }
.stat-item.rejected .stat-icon { background: #f56c6c; }
.stat-item.total .stat-icon { background: #409eff; }

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
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

.batch-approve-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-approve-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
}

.batch-reject-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
  font-weight: 600;
  color: white;
}

.batch-reject-btn:disabled {
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

/* 企业详情 */
.enterprise-detail {
  padding: 20px 0;
}

.verify-materials {
  margin-top: 24px;
}

.verify-materials h4 {
  margin-bottom: 16px;
  color: #1f2937;
  font-weight: 600;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
}

.material-item {
  text-align: center;
  padding: 12px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.material-item p {
  margin: 8px 0 0 0;
  font-size: 12px;
  color: #6b7280;
}

.verify-actions {
  margin-top: 24px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
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

/* 图片预览样式 */
:deep(.el-image) {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(59, 130, 246, 0.1);
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
}

.view-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  color: white;
}

.view-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.approve-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
}

.approve-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.reject-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
  color: white;
}

.reject-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.status-info {
  display: flex;
  align-items: center;
  margin-left: 8px;
}

/* 确保按钮在小屏幕上也能正常显示 */
@media (max-width: 1200px) {
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
:deep(.el-table tbody tr:hover .action-btn) {
  transform: translateY(-1px);
}
</style>
