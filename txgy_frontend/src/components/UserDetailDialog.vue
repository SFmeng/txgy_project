<template>
  <el-dialog
    v-model="visible"
    :title="`用户详情 - ${userInfo.real_name || userInfo.username}`"
    width="1200px"
    :before-close="handleClose"
    class="user-detail-dialog"
  >
    <div class="user-detail-content">
      <el-row :gutter="20">
        <!-- 左侧用户信息卡片 -->
        <el-col :span="8">
          <el-card class="user-profile-card">
            <template #header>
              <div class="card-header">
                <el-icon class="header-icon"><User /></el-icon>
                <span class="header-title">用户信息</span>
              </div>
            </template>

            <!-- 用户头像和基本信息 -->
            <div class="user-avatar-section">
              <el-avatar :size="100" :src="userInfo.avatar" class="user-avatar">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <div class="user-basic-info">
                <h3 class="user-name">{{ userInfo.real_name || userInfo.username }}</h3>
                <p class="user-username">@{{ userInfo.username }}</p>
                <div class="user-tags">
                  <el-tag :type="getStatusType(userInfo.status)" size="small">
                    {{ getStatusText(userInfo.status) }}
                  </el-tag>
                  <el-tag type="info" size="small">{{ getUserTypeText(userInfo.user_type) }}</el-tag>
                </div>
              </div>
            </div>

            <!-- 用户统计 -->
            <div class="user-stats">
              <div class="stat-item">
                <div class="stat-value">{{ userStats.loginCount }}</div>
                <div class="stat-label">登录次数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userStats.lastLoginDays }}</div>
                <div class="stat-label">天前登录</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userStats.accountAge }}</div>
                <div class="stat-label">账户天数</div>
              </div>
            </div>

            <!-- 联系信息 -->
            <div class="contact-info">
              <div class="info-item" v-if="userInfo.email">
                <el-icon class="info-icon"><Message /></el-icon>
                <span class="info-text">{{ userInfo.email }}</span>
              </div>
              <div class="info-item" v-if="userInfo.phone">
                <el-icon class="info-icon"><Phone /></el-icon>
                <span class="info-text">{{ userInfo.phone }}</span>
              </div>
              <div class="info-item" v-if="userInfo.address">
                <el-icon class="info-icon"><Location /></el-icon>
                <span class="info-text">{{ userInfo.address }}</span>
              </div>
            </div>
          </el-card>

          <!-- 最近活动 -->
          <el-card class="activity-card">
            <template #header>
              <div class="card-header">
                <el-icon class="header-icon"><Clock /></el-icon>
                <span class="header-title">最近活动</span>
              </div>
            </template>
            <div class="activity-list">
              <div v-for="activity in userActivities" :key="activity.id" class="activity-item">
                <div class="activity-icon">
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

        <!-- 右侧详细信息 -->
        <el-col :span="16">
          <el-card class="detail-info-card">
            <template #header>
              <el-tabs v-model="activeTab" class="detail-tabs">
                <el-tab-pane label="基本信息" name="basic">
                  <template #label>
                    <span class="tab-label">
                      <el-icon><User /></el-icon>
                      基本信息
                    </span>
                  </template>
                </el-tab-pane>
                <el-tab-pane label="权限角色" name="permissions">
                  <template #label>
                    <span class="tab-label">
                      <el-icon><Key /></el-icon>
                      权限角色
                    </span>
                  </template>
                </el-tab-pane>
                <el-tab-pane label="登录记录" name="logs">
                  <template #label>
                    <span class="tab-label">
                      <el-icon><Document /></el-icon>
                      登录记录
                    </span>
                  </template>
                </el-tab-pane>
                <el-tab-pane label="操作日志" name="operations">
                  <template #label>
                    <span class="tab-label">
                      <el-icon><List /></el-icon>
                      操作日志
                    </span>
                  </template>
                </el-tab-pane>
              </el-tabs>
            </template>

            <!-- 基本信息 -->
            <div v-show="activeTab === 'basic'" class="tab-content">
              <div class="info-grid">
                <div class="info-row">
                  <div class="info-item-detail">
                    <label class="info-label">用户ID</label>
                    <span class="info-value">{{ userInfo.user_id }}</span>
                  </div>
                  <div class="info-item-detail">
                    <label class="info-label">用户名</label>
                    <span class="info-value">{{ userInfo.username }}</span>
                  </div>
                </div>
                
                <div class="info-row">
                  <div class="info-item-detail">
                    <label class="info-label">真实姓名</label>
                    <span class="info-value">{{ userInfo.real_name || '-' }}</span>
                  </div>
                  <div class="info-item-detail">
                    <label class="info-label">性别</label>
                    <span class="info-value">{{ getGenderText(userInfo.gender) }}</span>
                  </div>
                </div>

                <div class="info-row">
                  <div class="info-item-detail">
                    <label class="info-label">邮箱地址</label>
                    <span class="info-value">{{ userInfo.email || '-' }}</span>
                  </div>
                  <div class="info-item-detail">
                    <label class="info-label">手机号码</label>
                    <span class="info-value">{{ userInfo.phone || '-' }}</span>
                  </div>
                </div>

                <div class="info-row">
                  <div class="info-item-detail">
                    <label class="info-label">注册时间</label>
                    <span class="info-value">{{ formatDateTime(userInfo.created_at) }}</span>
                  </div>
                  <div class="info-item-detail">
                    <label class="info-label">最后登录</label>
                    <span class="info-value">{{ formatDateTime(userInfo.last_login_at) }}</span>
                  </div>
                </div>

                <div class="info-row full-width">
                  <div class="info-item-detail">
                    <label class="info-label">个人简介</label>
                    <span class="info-value">{{ userInfo.bio || '暂无个人简介' }}</span>
                  </div>
                </div>

                <div class="info-row full-width">
                  <div class="info-item-detail">
                    <label class="info-label">地址</label>
                    <span class="info-value">{{ userInfo.address || '-' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 权限角色 -->
            <div v-show="activeTab === 'permissions'" class="tab-content">
              <div class="permissions-section">
                <h4 class="section-title">用户角色</h4>
                <div class="roles-list">
                  <el-tag
                    v-for="role in userRoles"
                    :key="role.id"
                    type="primary"
                    size="large"
                    class="role-tag"
                  >
                    {{ role.name }}
                  </el-tag>
                </div>
              </div>

              <el-divider />

              <div class="permissions-section">
                <h4 class="section-title">权限列表</h4>
                <div class="permissions-grid">
                  <div
                    v-for="permission in userPermissions"
                    :key="permission.id"
                    class="permission-item"
                  >
                    <el-icon class="permission-icon"><Key /></el-icon>
                    <div class="permission-info">
                      <div class="permission-name">{{ permission.name }}</div>
                      <div class="permission-desc">{{ permission.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 登录记录 -->
            <div v-show="activeTab === 'logs'" class="tab-content">
              <el-table :data="loginLogs" class="logs-table">
                <el-table-column label="登录时间" width="180">
                  <template #default="scope">
                    {{ formatDateTime(scope.row.loginTime) }}
                  </template>
                </el-table-column>
                <el-table-column label="IP地址" prop="ip" width="150" />
                <el-table-column label="登录地点" prop="location" />
                <el-table-column label="设备信息" prop="device" />
                <el-table-column label="状态" width="100">
                  <template #default="scope">
                    <el-tag :type="scope.row.success ? 'success' : 'danger'" size="small">
                      {{ scope.row.success ? '成功' : '失败' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- 操作日志 -->
            <div v-show="activeTab === 'operations'" class="tab-content">
              <el-table :data="operationLogs" class="logs-table">
                <el-table-column label="操作时间" width="180">
                  <template #default="scope">
                    {{ formatDateTime(scope.row.operationTime) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作类型" prop="type" width="120">
                  <template #default="scope">
                    <el-tag :type="getOperationTypeColor(scope.row.type)" size="small">
                      {{ scope.row.type }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作描述" prop="description" />
                <el-table-column label="IP地址" prop="ip" width="150" />
              </el-table>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleEdit">编辑用户</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import {
  User, UserFilled, Message, Phone, Location, Clock, Key, Document, List
} from '@element-plus/icons-vue'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  userInfo: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'edit'])

// 响应式数据
const activeTab = ref('basic')

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 模拟用户统计数据
const userStats = reactive({
  loginCount: 156,
  lastLoginDays: 2,
  accountAge: 365
})

// 模拟用户活动
const userActivities = ref([
  {
    id: 1,
    title: '登录系统',
    time: new Date(),
    icon: 'User'
  },
  {
    id: 2,
    title: '修改个人信息',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000),
    icon: 'Edit'
  },
  {
    id: 3,
    title: '查看用户列表',
    time: new Date(Date.now() - 5 * 60 * 60 * 1000),
    icon: 'View'
  }
])

// 模拟用户角色
const userRoles = ref([
  { id: 1, name: '系统管理员' },
  { id: 2, name: '内容管理员' }
])

// 模拟用户权限
const userPermissions = ref([
  { id: 1, name: 'user:view', description: '查看用户' },
  { id: 2, name: 'user:create', description: '创建用户' },
  { id: 3, name: 'user:edit', description: '编辑用户' },
  { id: 4, name: 'user:delete', description: '删除用户' },
  { id: 5, name: 'role:manage', description: '角色管理' },
  { id: 6, name: 'menu:manage', description: '菜单管理' }
])

// 模拟登录记录
const loginLogs = ref([
  {
    id: 1,
    loginTime: new Date(),
    ip: '192.168.1.100',
    location: '北京市',
    device: 'Chrome 120.0 / Windows 10',
    success: true
  },
  {
    id: 2,
    loginTime: new Date(Date.now() - 24 * 60 * 60 * 1000),
    ip: '192.168.1.101',
    location: '上海市',
    device: 'Safari 17.0 / macOS',
    success: true
  },
  {
    id: 3,
    loginTime: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    ip: '192.168.1.102',
    location: '广州市',
    device: 'Firefox 119.0 / Ubuntu',
    success: false
  }
])

// 模拟操作日志
const operationLogs = ref([
  {
    id: 1,
    operationTime: new Date(),
    type: '创建',
    description: '创建了新用户 "张三"',
    ip: '192.168.1.100'
  },
  {
    id: 2,
    operationTime: new Date(Date.now() - 60 * 60 * 1000),
    type: '修改',
    description: '修改了用户 "李四" 的基本信息',
    ip: '192.168.1.100'
  },
  {
    id: 3,
    operationTime: new Date(Date.now() - 2 * 60 * 60 * 1000),
    type: '删除',
    description: '删除了用户 "王五"',
    ip: '192.168.1.100'
  }
])

// 方法
const getStatusType = (status) => {
  return status === 'active' ? 'success' : 'danger'
}

const getStatusText = (status) => {
  return status === 'active' ? '正常' : '禁用'
}

const getUserTypeText = (type) => {
  const typeMap = {
    admin: '管理员',
    user: '普通用户',
    guest: '访客'
  }
  return typeMap[type] || '未知'
}

const getGenderText = (gender) => {
  const genderMap = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[gender] || '未设置'
}

const getOperationTypeColor = (type) => {
  const colorMap = {
    '创建': 'success',
    '修改': 'warning',
    '删除': 'danger',
    '查看': 'info'
  }
  return colorMap[type] || 'info'
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

const formatDateTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const handleClose = () => {
  visible.value = false
  activeTab.value = 'basic'
}

const handleEdit = () => {
  emit('edit', props.userInfo)
  handleClose()
}

// 监听对话框打开，重置标签页
watch(visible, (newVal) => {
  if (newVal) {
    activeTab.value = 'basic'
  }
})
</script>

<style scoped>
.user-detail-dialog {
  --el-dialog-border-radius: 12px;
}

.user-detail-content {
  padding: 0;
}

/* 卡片样式 */
.user-profile-card, .activity-card, .detail-info-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #409eff;
  font-size: 16px;
}

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

/* 用户头像区域 */
.user-avatar-section {
  text-align: center;
  padding: 20px 0;
}

.user-avatar {
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.user-basic-info {
  text-align: center;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #303133;
}

.user-username {
  font-size: 14px;
  color: #909399;
  margin: 0 0 12px 0;
}

.user-tags {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

/* 用户统计 */
.user-stats {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  margin: 16px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 联系信息 */
.contact-info {
  padding: 16px 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-icon {
  color: #409eff;
  font-size: 14px;
}

.info-text {
  font-size: 14px;
  color: #606266;
}

/* 活动列表 */
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
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #409eff;
  font-size: 12px;
}

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

/* 标签页 */
.detail-tabs {
  margin-bottom: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.tab-content {
  padding: 16px;
}

/* 基本信息网格 */
.info-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  gap: 20px;
}

.info-row.full-width {
  flex-direction: column;
}

.info-item-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: #303133;
  word-break: break-all;
}

/* 权限角色 */
.permissions-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
}

.roles-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.role-tag {
  font-size: 12px;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.permission-icon {
  color: #409eff;
  font-size: 14px;
}

.permission-info {
  flex: 1;
}

.permission-name {
  font-size: 12px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 2px;
}

.permission-desc {
  font-size: 11px;
  color: #909399;
}

/* 表格 */
.logs-table {
  width: 100%;
}

/* 对话框底部 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-detail-dialog {
    width: 95% !important;
  }

  .info-row {
    flex-direction: column;
    gap: 12px;
  }

  .user-stats {
    flex-direction: column;
    gap: 12px;
  }

  .permissions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
