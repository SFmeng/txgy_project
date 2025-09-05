<template>
  <div class="enterprise-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><OfficeBuilding /></el-icon>
            企业管理
          </h1>
          <p class="page-description">管理企业认证和企业信息</p>
        </div>
        <div class="header-actions">
          <el-button type="success" @click="handleExportData">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
          <el-button type="primary" @click="handleRefreshData">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
        </div>
      </div>
    </div>

    <!-- 企业管理导航和内容 -->
    <el-row :gutter="20">
      <!-- 左侧导航菜单 -->
      <el-col :span="5">
        <el-card class="enterprise-nav-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Menu /></el-icon>
              <span class="nav-title">管理模块</span>
            </div>
          </template>
          <el-menu
            :default-active="currentEnterprisePath"
            class="enterprise-nav"
            @select="handleNavSelect"
          >
            <el-menu-item index="/admin/enterprise/verify">
              <el-icon><DocumentChecked /></el-icon>
              <span>企业认证</span>
            </el-menu-item>
            <el-menu-item index="/admin/enterprise/manage">
              <el-icon><Shop /></el-icon>
              <span>企业管理</span>
            </el-menu-item>
          </el-menu>
        </el-card>

        <!-- 企业统计卡片 -->
        <el-card class="enterprise-stats-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><DataBoard /></el-icon>
              <span class="nav-title">企业统计</span>
            </div>
          </template>
          <div class="stats-list">
            <div class="stat-item">
              <div class="stat-label">待认证企业</div>
              <el-tag type="warning" size="small">{{ enterpriseStats.pending }}</el-tag>
            </div>
            <div class="stat-item">
              <div class="stat-label">已认证企业</div>
              <el-tag type="success" size="small">{{ enterpriseStats.verified }}</el-tag>
            </div>
            <div class="stat-item">
              <div class="stat-label">认证失败</div>
              <el-tag type="danger" size="small">{{ enterpriseStats.rejected }}</el-tag>
            </div>
            <div class="stat-item">
              <div class="stat-label">总企业数</div>
              <el-tag type="info" size="small">{{ enterpriseStats.total }}</el-tag>
            </div>
          </div>
        </el-card>

        <!-- 快速操作 -->
        <el-card class="quick-operations-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Lightning /></el-icon>
              <span class="nav-title">快速操作</span>
            </div>
          </template>
          <div class="quick-operations">
            <el-button type="primary" size="small" @click="handleQuickVerify">
              <el-icon><DocumentChecked /></el-icon>
              批量认证
            </el-button>
            <el-button type="success" size="small" @click="handleExportReport">
              <el-icon><Document /></el-icon>
              导出报告
            </el-button>
            <el-button type="warning" size="small" @click="handleSendNotification">
              <el-icon><Message /></el-icon>
              发送通知
            </el-button>
            <el-button type="info" size="small" @click="handleViewAnalytics">
              <el-icon><TrendCharts /></el-icon>
              查看分析
            </el-button>
          </div>
        </el-card>

        <!-- 最近活动 -->
        <el-card class="recent-activity-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Clock /></el-icon>
              <span class="nav-title">最近活动</span>
            </div>
          </template>
          <div class="activity-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon" :class="activity.type">
                <el-icon><component :is="activity.icon" /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ formatTime(activity.time) }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧企业管理内容 -->
      <el-col :span="19">
        <div class="enterprise-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  OfficeBuilding, Download, Refresh, Menu, DocumentChecked, Shop, DataBoard,
  Lightning, Document, Message, TrendCharts, Clock
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 响应式数据
const refreshLoading = ref(false)

// 当前企业管理路径
const currentEnterprisePath = computed(() => route.path)

// 企业统计数据
const enterpriseStats = ref({
  pending: 12,
  verified: 156,
  rejected: 8,
  total: 176
})

// 最近活动
const recentActivities = ref([
  {
    id: 1,
    title: '新企业提交认证申请',
    time: new Date(),
    icon: 'DocumentChecked',
    type: 'verify'
  },
  {
    id: 2,
    title: '企业认证审核通过',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000),
    icon: 'SuccessFilled',
    type: 'success'
  },
  {
    id: 3,
    title: '企业信息更新',
    time: new Date(Date.now() - 5 * 60 * 60 * 1000),
    icon: 'Edit',
    type: 'edit'
  },
  {
    id: 4,
    title: '企业认证被拒绝',
    time: new Date(Date.now() - 8 * 60 * 60 * 1000),
    icon: 'Warning',
    type: 'warning'
  }
])

// 方法
const handleNavSelect = (path) => {
  router.push(path)
}

const handleExportData = () => {
  ElMessage.success('企业数据导出功能开发中...')
}

const handleRefreshData = async () => {
  try {
    refreshLoading.value = true
    
    // 模拟刷新数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新失败:', error)
    ElMessage.error('数据刷新失败')
  } finally {
    refreshLoading.value = false
  }
}

const handleQuickVerify = () => {
  router.push('/admin/enterprise/verify')
  ElMessage.info('跳转到企业认证页面')
}

const handleExportReport = () => {
  ElMessage.success('企业报告导出功能开发中...')
}

const handleSendNotification = () => {
  ElMessage.success('批量通知功能开发中...')
}

const handleViewAnalytics = () => {
  ElMessage.success('企业分析功能开发中...')
}

const formatTime = (time) => {
  const now = new Date()
  const diff = now - time
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (minutes < 60) {
    return `${minutes}分钟前`
  } else if (hours < 24) {
    return `${hours}小时前`
  } else {
    return `${days}天前`
  }
}

// 生命周期
onMounted(() => {
  // 如果当前路径是 /admin/enterprise，重定向到企业认证
  if (route.path === '/admin/enterprise') {
    router.replace('/admin/enterprise/verify')
  }
})
</script>

<style scoped>
.enterprise-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  color: white;
  box-shadow: 0 4px 20px rgba(255, 154, 158, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-description {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

/* 左侧导航 */
.enterprise-nav-card, .enterprise-stats-card, .quick-operations-card, .recent-activity-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.nav-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-icon {
  color: #409eff;
  font-size: 16px;
}

.nav-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.enterprise-nav {
  border: none;
}

.enterprise-nav .el-menu-item {
  border-radius: 8px;
  margin: 4px 0;
  transition: all 0.3s;
}

.enterprise-nav .el-menu-item:hover {
  background: #fff2e8;
  color: #ff9a9e;
}

.enterprise-nav .el-menu-item.is-active {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
}

/* 统计列表 */
.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.stat-label {
  font-size: 13px;
  color: #606266;
}

/* 快速操作 */
.quick-operations {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-operations .el-button {
  justify-content: flex-start;
  text-align: left;
}

/* 最近活动 */
.activity-list {
  max-height: 200px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
}

.activity-icon.verify { background: #409eff; }
.activity-icon.success { background: #67c23a; }
.activity-icon.edit { background: #e6a23c; }
.activity-icon.warning { background: #f56c6c; }

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 13px;
  color: #303133;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 11px;
  color: #909399;
}

/* 右侧内容区域 */
.enterprise-content {
  min-height: 600px;
}

/* 过渡动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .enterprise-page .el-col:first-child {
    margin-bottom: 20px;
  }
}

@media (max-width: 768px) {
  .enterprise-page {
    padding: 12px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style>
