<template>
  <div class="admin-dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">管理仪表盘</h1>
          <p class="page-subtitle">实时监控系统运行状态和数据统计</p>
        </div>
        <div class="header-info">
          <div class="time-info">
            <el-icon class="time-icon"><Clock /></el-icon>
            <span>{{ currentTime }}</span>
          </div>
          <div class="weather-info">
            <el-icon class="weather-icon"><Sunny /></el-icon>
            <span>{{ weatherInfo }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="user-greeting">
          <el-avatar :size="60" :src="userInfo?.avatar" class="user-avatar">
            <el-icon><UserFilled /></el-icon>
          </el-avatar>
          <div class="greeting-text">
            <h2 class="welcome-title">
              欢迎回来，{{ userInfo?.real_name || userInfo?.username }}
            </h2>
            <p class="welcome-subtitle">
              今天是美好的一天，让我们开始工作吧！
            </p>
          </div>
        </div>
      </div>
      <div class="welcome-stats">
        <div class="stat-item">
          <div class="stat-number">{{ todayStats.visits || 0 }}</div>
          <div class="stat-label">今日访问</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ todayStats.users || 0 }}</div>
          <div class="stat-label">活跃用户</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ todayStats.orders || 0 }}</div>
          <div class="stat-label">新增订单</div>
        </div>
      </div>
    </div>

    <!-- 数据统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card" v-for="stat in statsData" :key="stat.key">
        <div class="stat-content">
          <div class="stat-icon" :style="{ backgroundColor: stat.color }">
            <el-icon :size="24">
              <component :is="stat.icon" />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-title">{{ stat.title }}</div>
            <div class="stat-trend" :class="stat.trend > 0 ? 'positive' : 'negative'">
              <el-icon>
                <ArrowUp v-if="stat.trend > 0" />
                <ArrowDown v-else />
              </el-icon>
              {{ Math.abs(stat.trend) }}%
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 主要内容区域 -->
    <el-row :gutter="20" class="main-content-section">
      <!-- 左侧：数据可视化和趋势 -->
      <el-col :span="16">
        <!-- 访问趋势图表 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">访问趋势分析</span>
              <div class="chart-controls">
                <el-radio-group v-model="chartTimeRange" size="small">
                  <el-radio-button value="7d">7天</el-radio-button>
                  <el-radio-button value="30d">30天</el-radio-button>
                  <el-radio-button value="90d">90天</el-radio-button>
                </el-radio-group>
              </div>
            </div>
          </template>
          <div class="chart-container" ref="visitChartRef">
            <!-- 模拟图表数据 -->
            <div class="chart-placeholder">
              <div class="chart-bars">
                <div v-for="(bar, index) in chartData" :key="index" class="chart-bar">
                  <div class="bar-fill" :style="{ height: bar.height + '%', backgroundColor: bar.color }"></div>
                  <div class="bar-label">{{ bar.label }}</div>
                </div>
              </div>
              <div class="chart-legend">
                <div class="legend-item">
                  <div class="legend-color" style="background: #409eff;"></div>
                  <span>页面访问</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color" style="background: #67c23a;"></div>
                  <span>用户活跃</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color" style="background: #e6a23c;"></div>
                  <span>新增注册</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 实时监控面板 -->
        <el-card class="monitor-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">实时监控</span>
              <el-tag type="success" size="small">
                <el-icon><CircleCheck /></el-icon>
                系统正常
              </el-tag>
            </div>
          </template>
          <div class="monitor-grid">
            <div class="monitor-item">
              <div class="monitor-icon cpu">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="monitor-info">
                <div class="monitor-label">CPU使用率</div>
                <div class="monitor-value">{{ systemStatus.cpu }}%</div>
                <el-progress :percentage="systemStatus.cpu" :show-text="false" :stroke-width="4" />
              </div>
            </div>
            <div class="monitor-item">
              <div class="monitor-icon memory">
                <el-icon><Cpu /></el-icon>
              </div>
              <div class="monitor-info">
                <div class="monitor-label">内存使用</div>
                <div class="monitor-value">{{ systemStatus.memory }}%</div>
                <el-progress :percentage="systemStatus.memory" :show-text="false" :stroke-width="4" color="#67c23a" />
              </div>
            </div>
            <div class="monitor-item">
              <div class="monitor-icon disk">
                <el-icon><FolderOpened /></el-icon>
              </div>
              <div class="monitor-info">
                <div class="monitor-label">磁盘空间</div>
                <div class="monitor-value">{{ systemStatus.disk }}%</div>
                <el-progress :percentage="systemStatus.disk" :show-text="false" :stroke-width="4" color="#e6a23c" />
              </div>
            </div>
            <div class="monitor-item">
              <div class="monitor-icon network">
                <el-icon><Connection /></el-icon>
              </div>
              <div class="monitor-info">
                <div class="monitor-label">网络流量</div>
                <div class="monitor-value">{{ systemStatus.network }} MB/s</div>
                <el-progress :percentage="75" :show-text="false" :stroke-width="4" color="#f56c6c" />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：快捷操作和通知 -->
      <el-col :span="8">
        <!-- 快捷操作 -->
        <el-card class="quick-actions-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">快捷操作</span>
            </div>
          </template>
          <div class="quick-actions-grid">
            <div class="action-item" @click="handleQuickAction('users')">
              <div class="action-icon users">
                <el-icon><User /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">用户管理</div>
                <div class="action-desc">管理系统用户</div>
              </div>
            </div>
            <div class="action-item" @click="handleQuickAction('roles')">
              <div class="action-icon roles">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">角色管理</div>
                <div class="action-desc">配置用户角色</div>
              </div>
            </div>
            <div class="action-item" @click="handleQuickAction('menus')">
              <div class="action-icon menus">
                <el-icon><Menu /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">菜单管理</div>
                <div class="action-desc">管理系统菜单</div>
              </div>
            </div>
            <div class="action-item" @click="handleQuickAction('settings')">
              <div class="action-icon settings">
                <el-icon><Setting /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">系统设置</div>
                <div class="action-desc">配置系统参数</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 待办事项 -->
        <el-card class="todo-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">待办事项</span>
              <el-badge :value="todoList.filter(t => !t.completed).length" class="todo-badge">
                <el-button type="primary" size="small" @click="showAddTodo = true">
                  <el-icon><Plus /></el-icon>
                </el-button>
              </el-badge>
            </div>
          </template>
          <div class="todo-list">
            <div v-for="todo in todoList" :key="todo.id" class="todo-item" :class="{ completed: todo.completed }">
              <el-checkbox v-model="todo.completed" @change="handleTodoChange(todo)">
                {{ todo.title }}
              </el-checkbox>
              <div class="todo-time">{{ todo.time }}</div>
            </div>
            <div v-if="todoList.length === 0" class="empty-todo">
              <el-empty description="暂无待办事项" :image-size="60" />
            </div>
          </div>
        </el-card>

        <!-- 系统通知 -->
        <el-card class="notification-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">系统通知</span>
              <el-badge :value="notifications.filter(n => !n.read).length" class="notification-badge">
                <el-button type="text" size="small" @click="markAllAsRead">全部已读</el-button>
              </el-badge>
            </div>
          </template>
          <div class="notification-list">
            <div v-for="notification in notifications" :key="notification.id"
                 class="notification-item"
                 :class="{ unread: !notification.read }"
                 @click="handleNotificationClick(notification)">
              <div class="notification-icon" :class="notification.type">
                <el-icon>
                  <component :is="getNotificationIcon(notification.type)" />
                </el-icon>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-desc">{{ notification.description }}</div>
                <div class="notification-time">{{ notification.time }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新动态和系统信息 -->
    <el-row :gutter="20" class="bottom-section">
      <el-col :span="12">
        <el-card title="最新动态" class="activity-card">
          <div class="activity-list">
            <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
              <div class="activity-avatar">
                <el-avatar :size="32" :src="activity.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
              </div>
              <div class="activity-content">
                <div class="activity-text">{{ activity.content }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card title="系统信息" class="system-info-card">
          <div class="system-info">
            <div class="info-item">
              <span class="info-label">服务器状态</span>
              <el-tag type="success">正常运行</el-tag>
            </div>
            <div class="info-item">
              <span class="info-label">数据库状态</span>
              <el-tag type="success">连接正常</el-tag>
            </div>
            <div class="info-item">
              <span class="info-label">缓存状态</span>
              <el-tag type="success">运行正常</el-tag>
            </div>
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span>v1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">最后更新</span>
              <span>{{ lastUpdateTime }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '@/api/auth'
import { ElMessage } from 'element-plus'
import {
  User,
  UserFilled,
  Lock,
  Document,
  Setting,
  FolderOpened,
  ArrowUp,
  ArrowDown,
  DataBoard,
  Shop,
  ChatDotRound,
  Bell,
  Clock,
  Sunny,
  Monitor,
  Cpu,
  Connection,
  CircleCheck,
  Menu,
  Plus,
  Warning,
  InfoFilled,
  SuccessFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const currentTime = ref('')
const weatherInfo = ref('晴朗 22°C')
const visitChartRef = ref()
const chartTimeRange = ref('7d')
const showAddTodo = ref(false)

const userInfo = computed(() => authStore.userInfo)

// 图表数据
const chartData = ref([
  { label: '周一', height: 65, color: '#409eff' },
  { label: '周二', height: 78, color: '#67c23a' },
  { label: '周三', height: 45, color: '#e6a23c' },
  { label: '周四', height: 89, color: '#409eff' },
  { label: '周五', height: 92, color: '#67c23a' },
  { label: '周六', height: 56, color: '#e6a23c' },
  { label: '周日', height: 73, color: '#409eff' }
])

// 系统状态监控
const systemStatus = ref({
  cpu: 45,
  memory: 68,
  disk: 32,
  network: 12.5
})

// 待办事项
const todoList = ref([
  { id: 1, title: '审核新用户注册申请', completed: false, time: '今天 14:30' },
  { id: 2, title: '更新系统安全策略', completed: false, time: '明天 09:00' },
  { id: 3, title: '备份数据库', completed: true, time: '昨天 18:00' },
  { id: 4, title: '检查服务器性能', completed: false, time: '本周五' }
])

// 系统通知
const notifications = ref([
  {
    id: 1,
    type: 'warning',
    title: '系统维护通知',
    description: '系统将于今晚22:00进行维护',
    time: '2小时前',
    read: false
  },
  {
    id: 2,
    type: 'success',
    title: '备份完成',
    description: '数据库备份已成功完成',
    time: '5小时前',
    read: false
  },
  {
    id: 3,
    type: 'info',
    title: '新用户注册',
    description: '有3个新用户注册待审核',
    time: '1天前',
    read: true
  }
])

// 今日统计数据
const todayStats = ref({
  visits: 1234,
  users: 89,
  orders: 56
})

// 统计数据
const statsData = ref([
  {
    key: 'users',
    title: '总用户数',
    value: '2,847',
    trend: 12.5,
    color: '#3b82f6',
    icon: 'User'
  },
  {
    key: 'orders',
    title: '总订单数',
    value: '1,429',
    trend: 8.2,
    color: '#10b981',
    icon: 'Shop'
  },
  {
    key: 'revenue',
    title: '总收入',
    value: '¥89,247',
    trend: -2.1,
    color: '#f59e0b',
    icon: 'DataBoard'
  },
  {
    key: 'messages',
    title: '消息数量',
    value: '342',
    trend: 15.8,
    color: '#8b5cf6',
    icon: 'ChatDotRound'
  }
])

// 加载状态
const loading = ref(false)

// 最新动态
const recentActivities = ref([
  {
    id: 1,
    content: '管理员 张三 创建了新的角色 "项目经理"',
    time: '2小时前',
    avatar: ''
  },
  {
    id: 2,
    content: '用户 李四 完成了企业认证',
    time: '4小时前',
    avatar: ''
  },
  {
    id: 3,
    content: '系统自动备份数据完成',
    time: '6小时前',
    avatar: ''
  },
  {
    id: 4,
    content: '新用户 王五 注册成功',
    time: '8小时前',
    avatar: ''
  }
])

const lastUpdateTime = ref('2024-01-15 10:30:00')

// 方法
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleQuickAction = (action) => {
  const routes = {
    users: '/admin/users',
    roles: '/admin/roles',
    permissions: '/admin/permissions',
    logs: '/admin/logs',
    settings: '/admin/settings',
    backup: '/admin/backup',
    menus: '/admin/menus'
  }

  if (routes[action]) {
    router.push(routes[action])
  }
}

// 待办事项相关方法
const handleTodoChange = (todo) => {
  console.log('待办事项状态变更:', todo)
  // 这里可以调用API保存状态
}

// 通知相关方法
const handleNotificationClick = (notification) => {
  notification.read = true
  console.log('点击通知:', notification)
  // 这里可以根据通知类型跳转到相应页面
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
  ElMessage.success('所有通知已标记为已读')
}

const getNotificationIcon = (type) => {
  const iconMap = {
    warning: 'Warning',
    success: 'SuccessFilled',
    info: 'InfoFilled',
    error: 'CircleClose'
  }
  return iconMap[type] || 'InfoFilled'
}

const initVisitChart = () => {
  // 这里可以集成图表库如 ECharts
  console.log('初始化访问趋势图表')
}

// 加载统计数据
const loadDashboardStats = async () => {
  loading.value = true
  try {
    // 尝试从API加载数据
    const response = await authAPI.getDashboardStats()
    const data = response.data

    // 更新今日统计
    todayStats.value = data.today_stats

    // 更新概览统计
    statsData.value = data.overview_stats

    console.log('Dashboard统计数据加载成功:', data)
  } catch (error) {
    console.warn('API加载失败，使用模拟数据:', error)
    // 使用模拟数据
    todayStats.value = {
      visits: 1234,
      users: 89,
      orders: 56
    }

    // 统计数据已经在初始化时设置了默认值
    console.log('使用模拟统计数据')
  } finally {
    loading.value = false
  }
}

let timeInterval = null

onMounted(() => {
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 60000) // 每分钟更新一次
  initVisitChart()
  loadDashboardStats()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.admin-dashboard {
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

.header-info {
  display: flex;
  gap: 24px;
  align-items: center;
}

.time-info, .weather-info {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.time-icon, .weather-icon {
  color: rgba(255, 255, 255, 0.9);
}

/* 欢迎区域 */
.welcome-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.user-greeting {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
}

.welcome-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1f2937;
}

.welcome-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.welcome-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.1);
  min-width: 100px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
  color: #3b82f6;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 4px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.stat-trend.positive {
  color: #10b981;
}

.stat-trend.negative {
  color: #ef4444;
}

.charts-section {
  margin-bottom: 24px;
}

.chart-card,
.quick-actions-card {
  height: 400px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.chart-container {
  height: 320px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 16px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 20px 0;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
}

.action-item:hover {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #dbeafe 0%, #f0f9ff 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.action-icon {
  font-size: 28px;
  color: #3b82f6;
}

.bottom-section {
  margin-bottom: 24px;
}

:deep(.el-card) {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  font-weight: 600;
  color: #1f2937;
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid rgba(59, 130, 246, 0.05);
  transition: all 0.3s ease;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background: rgba(59, 130, 246, 0.02);
  border-radius: 8px;
  margin: 0 -8px;
  padding: 16px 8px;
}

.activity-avatar {
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #374151;
  margin-bottom: 4px;
  line-height: 1.5;
}

.activity-time {
  font-size: 12px;
  color: #9ca3af;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.05);
}

.info-label {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

/* 状态标签样式 */
:deep(.el-tag) {
  border-radius: 6px;
  font-weight: 500;
}

:deep(.el-tag--success) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
}

/* 头像样式 */
:deep(.el-avatar) {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

@media (max-width: 1200px) {
  .header-info {
    flex-direction: column;
    gap: 12px;
  }

  .time-info, .weather-info {
    font-size: 14px;
  }
}

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

  .header-info {
    flex-direction: row;
    justify-content: center;
  }

  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: 24px;
    padding: 20px;
  }

  .user-greeting {
    flex-direction: column;
    text-align: center;
  }

  .welcome-stats {
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    grid-template-columns: 1fr;
  }

  .chart-card,
  .quick-actions-card {
    height: auto;
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .welcome-stats {
    flex-direction: column;
    align-items: center;
  }

  .stat-item {
    min-width: 120px;
  }

  .time-info, .weather-info {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* 新增样式 - 主要内容区域 */
.main-content-section {
  margin-bottom: 20px;
}

/* 图表卡片 */
.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart-controls .el-radio-group {
  margin-left: 16px;
}

.chart-container {
  height: 280px;
  padding: 20px;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-bars {
  display: flex;
  align-items: end;
  justify-content: space-around;
  height: 200px;
  padding: 0 20px;
}

.chart-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 40px;
}

.bar-fill {
  width: 100%;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
  min-height: 10px;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  color: #666;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #666;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

/* 实时监控 */
.monitor-card {
  margin-bottom: 20px;
}

.monitor-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.monitor-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.monitor-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.monitor-icon.cpu { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.monitor-icon.memory { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.monitor-icon.disk { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.monitor-icon.network { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }

.monitor-info {
  flex: 1;
}

.monitor-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.monitor-value {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

/* 快捷操作重新设计 */
.quick-actions-card {
  margin-bottom: 20px;
}

.quick-actions-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-actions-grid .action-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.quick-actions-grid .action-item:hover {
  background: #e3f2fd;
  border-color: #409eff;
  transform: translateX(4px);
}

.quick-actions-grid .action-icon {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.action-icon.users { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.action-icon.roles { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.action-icon.menus { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.action-icon.settings { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }

.action-content {
  flex: 1;
}

.action-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 2px;
}

.action-desc {
  font-size: 12px;
  color: #666;
}

/* 待办事项 */
.todo-card {
  margin-bottom: 20px;
}

.todo-badge {
  margin-left: 8px;
}

.todo-list {
  max-height: 200px;
  overflow-y: auto;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-item.completed :deep(.el-checkbox__label) {
  text-decoration: line-through;
}

.todo-time {
  font-size: 12px;
  color: #999;
}

.empty-todo {
  text-align: center;
  padding: 20px 0;
}

/* 系统通知 */
.notification-card {
  margin-bottom: 20px;
}

.notification-badge {
  margin-left: 8px;
}

.notification-list {
  max-height: 250px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f8f9fa;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: #f0f9ff;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  flex-shrink: 0;
}

.notification-icon.warning { background: #e6a23c; }
.notification-icon.success { background: #67c23a; }
.notification-icon.info { background: #409eff; }
.notification-icon.error { background: #f56c6c; }

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.notification-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 11px;
  color: #999;
}

/* 响应式优化 */
@media (max-width: 1200px) {
  .monitor-grid {
    grid-template-columns: 1fr;
  }

  .chart-bars {
    padding: 0 10px;
  }

  .chart-bar {
    width: 30px;
  }
}

@media (max-width: 768px) {
  .main-content-section .el-col {
    margin-bottom: 20px;
  }

  .chart-container {
    height: 200px;
    padding: 10px;
  }

  .chart-bars {
    height: 120px;
  }

  .monitor-item {
    padding: 12px;
  }

  .monitor-icon {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>
