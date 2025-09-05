<template>
  <div class="profile-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><User /></el-icon>
            个人中心
          </h1>
          <p class="page-description">管理您的个人信息和账户设置</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="handleSaveProfile" :loading="saveLoading">
            <el-icon><Check /></el-icon>
            保存更改
          </el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="20">
      <!-- 左侧个人信息卡片 -->
      <el-col :span="8">
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><User /></el-icon>
              <span class="header-title">个人信息</span>
            </div>
          </template>

          <!-- 头像区域 -->
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <el-avatar :size="120" :src="userProfile.avatar" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="avatar-overlay" @click="handleAvatarUpload">
                <el-icon><Camera /></el-icon>
                <span>更换头像</span>
              </div>
            </div>
            <div class="user-basic-info">
              <h3 class="username">{{ userProfile.real_name || userProfile.username }}</h3>
              <p class="user-role">{{ userProfile.role_name || '普通用户' }}</p>
              <el-tag :type="getStatusType(userProfile.status)" size="small">
                {{ getStatusText(userProfile.status) }}
              </el-tag>
            </div>
          </div>

          <!-- 统计信息 -->
          <div class="stats-section">
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

          <!-- 快速操作 -->
          <div class="quick-actions">
            <el-button type="primary" plain @click="activeTab = 'security'">
              <el-icon><Lock /></el-icon>
              安全设置
            </el-button>
            <el-button type="success" plain @click="activeTab = 'preferences'">
              <el-icon><Setting /></el-icon>
              偏好设置
            </el-button>
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
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
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
        <el-card class="detail-card">
          <template #header>
            <el-tabs v-model="activeTab" class="profile-tabs">
              <el-tab-pane label="基本信息" name="basic">
                <template #label>
                  <span class="tab-label">
                    <el-icon><User /></el-icon>
                    基本信息
                  </span>
                </template>
              </el-tab-pane>
              <el-tab-pane label="安全设置" name="security">
                <template #label>
                  <span class="tab-label">
                    <el-icon><Lock /></el-icon>
                    安全设置
                  </span>
                </template>
              </el-tab-pane>
              <el-tab-pane label="偏好设置" name="preferences">
                <template #label>
                  <span class="tab-label">
                    <el-icon><Setting /></el-icon>
                    偏好设置
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
            </el-tabs>
          </template>

          <!-- 基本信息表单 -->
          <div v-show="activeTab === 'basic'" class="tab-content">
            <el-form :model="userProfile" :rules="profileRules" ref="profileFormRef" label-width="100px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="userProfile.username" disabled>
                      <template #prefix>
                        <el-icon><User /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="真实姓名" prop="real_name">
                    <el-input v-model="userProfile.real_name" placeholder="请输入真实姓名">
                      <template #prefix>
                        <el-icon><UserFilled /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="userProfile.email" placeholder="请输入邮箱地址">
                      <template #prefix>
                        <el-icon><Message /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="userProfile.phone" placeholder="请输入手机号">
                      <template #prefix>
                        <el-icon><Phone /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-radio-group v-model="userProfile.gender">
                      <el-radio value="male">男</el-radio>
                      <el-radio value="female">女</el-radio>
                      <el-radio value="other">其他</el-radio>
                    </el-radio-group>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="生日" prop="birthday">
                    <el-date-picker
                      v-model="userProfile.birthday"
                      type="date"
                      placeholder="选择生日"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="个人简介" prop="bio">
                <el-input
                  v-model="userProfile.bio"
                  type="textarea"
                  :rows="4"
                  placeholder="介绍一下自己..."
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="地址" prop="address">
                <el-input v-model="userProfile.address" placeholder="请输入地址">
                  <template #prefix>
                    <el-icon><Location /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-form>
          </div>

          <!-- 安全设置 -->
          <div v-show="activeTab === 'security'" class="tab-content">
            <div class="security-section">
              <h3 class="section-title">密码安全</h3>
              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">登录密码</div>
                  <div class="security-desc">定期更换密码可以提高账户安全性</div>
                </div>
                <el-button type="primary" @click="showChangePassword = true">修改密码</el-button>
              </div>
            </div>

            <el-divider />

            <div class="security-section">
              <h3 class="section-title">两步验证</h3>
              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">手机验证</div>
                  <div class="security-desc">{{ userProfile.phone ? `已绑定手机：${userProfile.phone}` : '未绑定手机' }}</div>
                </div>
                <el-button :type="userProfile.phone ? 'success' : 'primary'">
                  {{ userProfile.phone ? '已绑定' : '绑定手机' }}
                </el-button>
              </div>

              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">邮箱验证</div>
                  <div class="security-desc">{{ userProfile.email ? `已绑定邮箱：${userProfile.email}` : '未绑定邮箱' }}</div>
                </div>
                <el-button :type="userProfile.email ? 'success' : 'primary'">
                  {{ userProfile.email ? '已绑定' : '绑定邮箱' }}
                </el-button>
              </div>
            </div>
          </div>

          <!-- 偏好设置 -->
          <div v-show="activeTab === 'preferences'" class="tab-content">
            <div class="preference-section">
              <h3 class="section-title">界面设置</h3>
              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">主题模式</div>
                  <div class="preference-desc">选择您喜欢的界面主题</div>
                </div>
                <el-radio-group v-model="preferences.theme">
                  <el-radio value="light">浅色</el-radio>
                  <el-radio value="dark">深色</el-radio>
                  <el-radio value="auto">跟随系统</el-radio>
                </el-radio-group>
              </div>

              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">语言设置</div>
                  <div class="preference-desc">选择界面显示语言</div>
                </div>
                <el-select v-model="preferences.language" style="width: 200px">
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                  <el-option label="繁體中文" value="zh-TW" />
                </el-select>
              </div>
            </div>

            <el-divider />

            <div class="preference-section">
              <h3 class="section-title">通知设置</h3>
              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">邮件通知</div>
                  <div class="preference-desc">接收重要消息的邮件通知</div>
                </div>
                <el-switch v-model="preferences.emailNotification" />
              </div>

              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">短信通知</div>
                  <div class="preference-desc">接收重要消息的短信通知</div>
                </div>
                <el-switch v-model="preferences.smsNotification" />
              </div>

              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">浏览器通知</div>
                  <div class="preference-desc">在浏览器中显示通知</div>
                </div>
                <el-switch v-model="preferences.browserNotification" />
              </div>
            </div>
          </div>

          <!-- 登录记录 -->
          <div v-show="activeTab === 'logs'" class="tab-content">
            <div class="logs-section">
              <div class="logs-header">
                <h3 class="section-title">登录记录</h3>
                <el-button type="primary" size="small" @click="refreshLogs">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>

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
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="showChangePassword" title="修改密码" width="500px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showChangePassword = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 头像上传 -->
    <input ref="avatarInput" type="file" accept="image/*" style="display: none" @change="handleAvatarChange" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import {
  User, UserFilled, Check, Camera, Lock, Setting, Clock, Document, Message, Phone, Location, Refresh
} from '@element-plus/icons-vue'

// Store
const authStore = useAuthStore()

// 响应式数据
const activeTab = ref('basic')
const saveLoading = ref(false)
const showChangePassword = ref(false)
const passwordLoading = ref(false)
const avatarInput = ref()
const profileFormRef = ref()
const passwordFormRef = ref()

// 用户资料
const userProfile = reactive({
  user_id: 1,
  username: 'admin',
  real_name: '系统管理员',
  email: 'admin@example.com',
  phone: '13800138000',
  gender: 'male',
  birthday: null,
  bio: '这是一个系统管理员账户',
  address: '北京市朝阳区',
  avatar: '',
  status: 'active',
  role_name: '超级管理员'
})

// 用户统计
const userStats = reactive({
  loginCount: 156,
  lastLoginDays: 0,
  accountAge: 365
})

// 偏好设置
const preferences = reactive({
  theme: 'light',
  language: 'zh-CN',
  emailNotification: true,
  smsNotification: false,
  browserNotification: true
})

// 密码表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 最近活动
const recentActivities = ref([
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

// 登录记录
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

// 表单验证规则
const profileRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const getStatusType = (status) => {
  return status === 'active' ? 'success' : 'danger'
}

const getStatusText = (status) => {
  return status === 'active' ? '正常' : '禁用'
}

// 方法
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
  return time.toLocaleString('zh-CN')
}

const handleSaveProfile = async () => {
  try {
    await profileFormRef.value?.validate()
    saveLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('个人信息保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saveLoading.value = false
  }
}

const handleAvatarUpload = () => {
  avatarInput.value?.click()
}

const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      userProfile.avatar = e.target.result
      ElMessage.success('头像上传成功')
    }
    reader.readAsDataURL(file)
  }
}

const handleChangePassword = async () => {
  try {
    await passwordFormRef.value?.validate()
    passwordLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('密码修改成功')
    showChangePassword.value = false

    // 重置表单
    Object.assign(passwordForm, {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error('修改密码失败')
  } finally {
    passwordLoading.value = false
  }
}

const refreshLogs = () => {
  ElMessage.success('登录记录已刷新')
}

// 生命周期
onMounted(() => {
  // 从store获取用户信息
  const userInfo = authStore.userInfo
  if (userInfo) {
    Object.assign(userProfile, userInfo)
  }
})
</script>

<style scoped>
.profile-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
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

.header-actions .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

/* 卡片样式 */
.profile-card, .activity-card, .detail-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #409eff;
  font-size: 18px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 头像区域 */
.avatar-section {
  text-align: center;
  padding: 20px 0;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.user-avatar {
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
  color: white;
  font-size: 12px;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.user-basic-info {
  text-align: center;
}

.username {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #303133;
}

.user-role {
  font-size: 14px;
  color: #909399;
  margin: 0 0 8px 0;
}

/* 统计信息 */
.stats-section {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  margin: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 快速操作 */
.quick-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding-top: 20px;
}

/* 活动列表 */
.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #409eff;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #909399;
}

/* 标签页 */
.profile-tabs {
  margin-bottom: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tab-content {
  padding: 20px;
}

/* 安全设置 */
.security-section, .preference-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.security-item, .preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.security-item:last-child, .preference-item:last-child {
  border-bottom: none;
}

.security-info, .preference-info {
  flex: 1;
}

.security-title, .preference-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.security-desc, .preference-desc {
  font-size: 12px;
  color: #909399;
}

/* 登录记录 */
.logs-section {
  padding: 0;
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.logs-table {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-page {
    padding: 12px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .stats-section {
    flex-direction: column;
    gap: 16px;
  }

  .quick-actions {
    flex-direction: column;
  }

  .security-item, .preference-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
