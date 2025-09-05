<template>
  <div class="enterprise-dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">
          欢迎回来，{{ authStore.userInfo?.enterprise_info?.company_name || '企业用户' }}
        </h1>
        <p class="welcome-subtitle">
          今天是 {{ currentDate }}，祝您工作愉快！
        </p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" @click="$router.push('/info/publish')">
          发布信息
        </el-button>
        <el-button @click="$router.push('/search')">
          搜索匹配
        </el-button>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><Shop /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.published_info }}</div>
            <div class="stat-label">已发布信息</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><View /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.total_views }}</div>
            <div class="stat-label">总浏览量</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.inquiries }}</div>
            <div class="stat-label">收到询价</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><DocumentChecked /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.orders }}</div>
            <div class="stat-label">成交订单</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <h2 class="section-title">快捷操作</h2>
      <div class="actions-grid">
        <div class="action-card" @click="$router.push('/info/supply')">
          <el-icon class="action-icon"><Goods /></el-icon>
          <div class="action-title">发布供应</div>
          <div class="action-desc">发布产品供应信息</div>
        </div>
        
        <div class="action-card" @click="$router.push('/info/demand')">
          <el-icon class="action-icon"><Search /></el-icon>
          <div class="action-title">发布需求</div>
          <div class="action-desc">发布采购需求信息</div>
        </div>
        
        <div class="action-card" @click="$router.push('/communication')">
          <el-icon class="action-icon"><ChatDotRound /></el-icon>
          <div class="action-title">消息中心</div>
          <div class="action-desc">查看询价和消息</div>
        </div>
        
        <div class="action-card" @click="$router.push('/business/orders')">
          <el-icon class="action-icon"><DocumentChecked /></el-icon>
          <div class="action-title">订单管理</div>
          <div class="action-desc">管理交易订单</div>
        </div>
      </div>
    </div>

    <!-- 最新动态 -->
    <div class="recent-activities">
      <h2 class="section-title">最新动态</h2>
      <el-card class="activities-card">
        <div class="activity-list">
          <div class="activity-item" v-for="activity in activities" :key="activity.id">
            <div class="activity-icon">
              <el-icon><component :is="activity.icon" /></el-icon>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {
  Shop,
  View,
  ChatDotRound,
  DocumentChecked,
  Goods,
  Search,
  Bell,
  User
} from '@element-plus/icons-vue'

const authStore = useAuthStore()

const stats = ref({
  published_info: 12,
  total_views: 1580,
  inquiries: 23,
  orders: 8
})

const activities = ref([
  {
    id: 1,
    icon: 'Bell',
    title: '您发布的"防腐涂料"收到新询价',
    time: '2小时前'
  },
  {
    id: 2,
    icon: 'DocumentChecked',
    title: '订单 #20240827001 已确认',
    time: '4小时前'
  },
  {
    id: 3,
    icon: 'User',
    title: '新用户关注了您的企业',
    time: '1天前'
  },
  {
    id: 4,
    icon: 'Shop',
    title: '您的供应信息"保温材料"已审核通过',
    time: '2天前'
  }
])

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

onMounted(() => {
  // TODO: 获取统计数据
  // fetchDashboardStats()
})
</script>

<style scoped>
.enterprise-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  border-radius: 12px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 16px;
  opacity: 0.9;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.stats-section {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: #f0f9ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 24px;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
}

.quick-actions {
  margin-bottom: 30px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 32px;
  color: #3b82f6;
  margin-bottom: 12px;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.action-desc {
  font-size: 14px;
  color: #6b7280;
}

.recent-activities {
  margin-bottom: 30px;
}

.activities-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  background: #f0f9ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 16px;
}

.activity-title {
  font-size: 14px;
  color: #1f2937;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
