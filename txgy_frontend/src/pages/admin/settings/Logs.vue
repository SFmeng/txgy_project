<template>
  <div class="logs-settings">
    <!-- 日志配置 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Document /></el-icon>
            <span class="header-title">日志配置</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleSave" :loading="saveLoading">
              <el-icon><Check /></el-icon>
              保存配置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="logsConfig" :rules="logsRules" ref="logsFormRef" label-width="120px">
        <div class="form-section">
          <h4 class="section-subtitle">日志级别设置</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="系统日志级别" prop="systemLevel">
                <el-select v-model="logsConfig.systemLevel" placeholder="请选择日志级别">
                  <el-option label="DEBUG" value="debug" />
                  <el-option label="INFO" value="info" />
                  <el-option label="WARNING" value="warning" />
                  <el-option label="ERROR" value="error" />
                  <el-option label="CRITICAL" value="critical" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="安全日志级别" prop="securityLevel">
                <el-select v-model="logsConfig.securityLevel" placeholder="请选择日志级别">
                  <el-option label="INFO" value="info" />
                  <el-option label="WARNING" value="warning" />
                  <el-option label="ERROR" value="error" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h4 class="section-subtitle">日志保留设置</h4>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="保留天数" prop="retentionDays">
                <el-input-number
                  v-model="logsConfig.retentionDays"
                  :min="1"
                  :max="365"
                  controls-position="right"
                />
                <span class="form-tip">天</span>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="最大文件大小" prop="maxFileSize">
                <el-input-number
                  v-model="logsConfig.maxFileSize"
                  :min="1"
                  :max="1024"
                  controls-position="right"
                />
                <span class="form-tip">MB</span>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="自动清理">
                <el-switch v-model="logsConfig.autoCleanup" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h4 class="section-subtitle">日志类型启用</h4>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="登录日志">
                <el-switch v-model="logsConfig.enableLogin" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="操作日志">
                <el-switch v-model="logsConfig.enableOperation" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="错误日志">
                <el-switch v-model="logsConfig.enableError" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="API日志">
                <el-switch v-model="logsConfig.enableAPI" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <!-- 日志统计 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><DataBoard /></el-icon>
            <span class="header-title">日志统计</span>
          </div>
          <div class="header-actions">
            <el-button type="warning" @click="handleClearAllLogs">
              <el-icon><Delete /></el-icon>
              清空所有日志
            </el-button>
          </div>
        </div>
      </template>

      <div class="logs-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon login">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ logsStats.loginCount }}</div>
                <div class="stat-label">登录日志</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon operation">
                <el-icon><Operation /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ logsStats.operationCount }}</div>
                <div class="stat-label">操作日志</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon error">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ logsStats.errorCount }}</div>
                <div class="stat-label">错误日志</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon api">
                <el-icon><Connection /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ logsStats.apiCount }}</div>
                <div class="stat-label">API日志</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 最近日志 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><List /></el-icon>
            <span class="header-title">最近日志</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleRefreshLogs">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="recentLogs" class="logs-table">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="level" label="级别" width="100">
          <template #default="scope">
            <el-tag :type="getLogLevelColor(scope.row.level)" size="small">
              {{ scope.row.level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="message" label="消息" />
        <el-table-column prop="ip" label="IP地址" width="150" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Check, DataBoard, List, Delete, Refresh, User, Operation, Warning, Connection
} from '@element-plus/icons-vue'

// 响应式数据
const saveLoading = ref(false)
const logsFormRef = ref()

// 日志配置
const logsConfig = reactive({
  systemLevel: 'info',
  securityLevel: 'warning',
  retentionDays: 30,
  maxFileSize: 100,
  autoCleanup: true,
  enableLogin: true,
  enableOperation: true,
  enableError: true,
  enableAPI: false
})

// 日志统计
const logsStats = reactive({
  loginCount: '1,234',
  operationCount: '5,678',
  errorCount: '23',
  apiCount: '12,456'
})

// 最近日志
const recentLogs = ref([
  {
    time: '2024-01-15 14:30:25',
    level: 'INFO',
    type: '登录',
    user: 'admin',
    message: '用户登录成功',
    ip: '192.168.1.100'
  },
  {
    time: '2024-01-15 14:25:10',
    level: 'WARNING',
    type: '操作',
    user: 'user1',
    message: '尝试访问未授权页面',
    ip: '192.168.1.101'
  },
  {
    time: '2024-01-15 14:20:05',
    level: 'ERROR',
    type: '系统',
    user: 'system',
    message: '数据库连接超时',
    ip: '127.0.0.1'
  }
])

// 表单验证规则
const logsRules = {
  retentionDays: [
    { required: true, message: '请设置日志保留天数', trigger: 'blur' }
  ],
  maxFileSize: [
    { required: true, message: '请设置最大文件大小', trigger: 'blur' }
  ]
}

// 方法
const handleSave = async () => {
  try {
    await logsFormRef.value?.validate()
    saveLoading.value = true
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('日志配置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoading.value = false
  }
}

const handleClearAllLogs = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有日志吗？此操作不可撤销！',
      '清空确认',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    recentLogs.value = []
    Object.keys(logsStats).forEach(key => {
      logsStats[key] = '0'
    })
    
    ElMessage.success('所有日志已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空日志失败:', error)
    }
  }
}

const handleRefreshLogs = () => {
  ElMessage.success('日志列表已刷新')
}

const getLogLevelColor = (level) => {
  const colorMap = {
    'DEBUG': 'info',
    'INFO': 'success',
    'WARNING': 'warning',
    'ERROR': 'danger',
    'CRITICAL': 'danger'
  }
  return colorMap[level] || 'info'
}
</script>

<style scoped>
.logs-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
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

.header-actions {
  display: flex;
  gap: 12px;
}

.form-section {
  margin: 20px 0;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.section-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.form-tip {
  margin-left: 8px;
  font-size: 12px;
  color: #909399;
}

.logs-stats {
  padding: 16px 0;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.stat-icon.login { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.operation { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-icon.error { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }
.stat-icon.api { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.logs-table {
  margin-top: 16px;
}
</style>
