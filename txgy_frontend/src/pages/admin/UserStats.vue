<template>
  <div class="user-stats-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">用户统计</h1>
        <p class="page-description">查看用户注册、活跃度和企业认证等统计数据</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon user-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ userStats.total_users }}</div>
                <div class="stats-label">总用户数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon enterprise-icon">
                <el-icon><OfficeBuilding /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ userStats.enterprise_users }}</div>
                <div class="stats-label">企业用户</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon individual-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ userStats.individual_users }}</div>
                <div class="stats-label">个人用户</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon verified-icon">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ userStats.verified_enterprises }}</div>
                <div class="stats-label">已认证企业</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>用户注册趋势</span>
            </template>
            <div id="userTrendChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>用户类型分布</span>
            </template>
            <div id="userTypeChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 企业认证状态统计 -->
    <div class="verify-stats-section">
      <el-card>
        <template #header>
          <span>企业认证状态统计</span>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="verify-stat-item pending">
              <div class="verify-stat-number">{{ verifyStats.pending }}</div>
              <div class="verify-stat-label">待审核</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="verify-stat-item approved">
              <div class="verify-stat-number">{{ verifyStats.approved }}</div>
              <div class="verify-stat-label">已通过</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="verify-stat-item rejected">
              <div class="verify-stat-number">{{ verifyStats.rejected }}</div>
              <div class="verify-stat-label">已拒绝</div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- 最近注册用户 -->
    <div class="recent-users-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>最近注册用户</span>
            <el-button type="text" @click="$router.push('/admin/users')">
              查看全部
            </el-button>
          </div>
        </template>
        
        <el-table :data="recentUsers" style="width: 100%">
          <el-table-column prop="username" label="用户名" width="120" />
          <el-table-column prop="real_name" label="真实姓名" width="120" />
          <el-table-column prop="user_type" label="用户类型" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.user_type === 'enterprise' ? 'warning' : 'primary'">
                {{ scope.row.user_type === 'enterprise' ? '企业' : '个人' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="phone" label="手机号" width="120" />
          <el-table-column prop="date_joined" label="注册时间" width="160">
            <template #default="scope">
              {{ formatDate(scope.row.date_joined) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="80">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                {{ scope.row.status === 'active' ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User, UserFilled, OfficeBuilding, CircleCheck
} from '@element-plus/icons-vue'
import { authAPI } from '@/api/auth'

// 响应式数据
const loading = ref(false)
const userStats = reactive({
  total_users: 0,
  enterprise_users: 0,
  individual_users: 0,
  verified_enterprises: 0
})

const verifyStats = reactive({
  pending: 0,
  approved: 0,
  rejected: 0
})

const recentUsers = ref([])

// 方法
const loadUserStats = async () => {
  loading.value = true
  try {
    // 获取用户列表进行统计
    const response = await authAPI.getUserList({ page_size: 1000 })
    const users = response.data.results || []
    
    // 统计用户数据
    userStats.total_users = users.length
    userStats.enterprise_users = users.filter(u => u.user_type === 'enterprise').length
    userStats.individual_users = users.filter(u => u.user_type === 'individual').length
    
    // 统计企业认证状态
    const enterprises = users.filter(u => u.user_type === 'enterprise')
    verifyStats.pending = enterprises.filter(u => 
      !u.enterprise_info || u.enterprise_info.verify_status === 'pending'
    ).length
    verifyStats.approved = enterprises.filter(u => 
      u.enterprise_info && u.enterprise_info.verify_status === 'approved'
    ).length
    verifyStats.rejected = enterprises.filter(u => 
      u.enterprise_info && u.enterprise_info.verify_status === 'rejected'
    ).length
    
    userStats.verified_enterprises = verifyStats.approved
    
    // 获取最近注册的用户（最新10个）
    recentUsers.value = users
      .sort((a, b) => new Date(b.date_joined) - new Date(a.date_joined))
      .slice(0, 10)
    
  } catch (error) {
    ElMessage.error('加载统计数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadUserStats()
})
</script>

<style scoped>
.user-stats-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 10px 0;
}

.page-description {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
}

.stats-cards {
  margin-bottom: 20px;
}

.stats-card {
  height: 120px;
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stats-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  margin-right: 20px;
}

.user-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.enterprise-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.individual-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.verified-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 32px;
  font-weight: 700;
  color: #2d3748;
  line-height: 1;
}

.stats-label {
  font-size: 14px;
  color: #718096;
  margin-top: 5px;
}

.charts-section {
  margin-bottom: 20px;
}

.verify-stats-section {
  margin-bottom: 20px;
}

.verify-stat-item {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.verify-stat-item:hover {
  transform: scale(1.05);
}

.verify-stat-item.pending {
  background: linear-gradient(135deg, #fef5e7, #fed7aa);
  border: 2px solid #f6ad55;
}

.verify-stat-item.approved {
  background: linear-gradient(135deg, #f0fff4, #c6f6d5);
  border: 2px solid #48bb78;
}

.verify-stat-item.rejected {
  background: linear-gradient(135deg, #fed7d7, #feb2b2);
  border: 2px solid #f56565;
}

.verify-stat-number {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 5px;
}

.verify-stat-item.pending .verify-stat-number {
  color: #d69e2e;
}

.verify-stat-item.approved .verify-stat-number {
  color: #38a169;
}

.verify-stat-item.rejected .verify-stat-number {
  color: #e53e3e;
}

.verify-stat-label {
  font-size: 16px;
  font-weight: 500;
}

.recent-users-section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
