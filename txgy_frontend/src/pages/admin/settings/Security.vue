<template>
  <div class="security-settings">
    <!-- 密码策略 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Lock /></el-icon>
            <span class="header-title">密码策略</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleSavePassword" :loading="savePasswordLoading">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="passwordConfig" :rules="passwordRules" ref="passwordFormRef" label-width="140px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最小密码长度" prop="minLength">
              <el-input-number
                v-model="passwordConfig.minLength"
                :min="6"
                :max="20"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="密码有效期" prop="expireDays">
              <el-input-number
                v-model="passwordConfig.expireDays"
                :min="0"
                :max="365"
                controls-position="right"
              />
              <span class="form-tip">天（0表示永不过期）</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="必须包含大写字母">
              <el-switch v-model="passwordConfig.requireUppercase" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="必须包含小写字母">
              <el-switch v-model="passwordConfig.requireLowercase" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="必须包含数字">
              <el-switch v-model="passwordConfig.requireNumbers" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="必须包含特殊字符">
              <el-switch v-model="passwordConfig.requireSpecialChars" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="禁止连续字符">
              <el-switch v-model="passwordConfig.forbidSequential" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="禁止重复字符">
              <el-switch v-model="passwordConfig.forbidRepeated" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 登录安全 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><User /></el-icon>
            <span class="header-title">登录安全</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleSaveLogin" :loading="saveLoginLoading">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="loginConfig" :rules="loginRules" ref="loginFormRef" label-width="140px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最大登录尝试次数" prop="maxAttempts">
              <el-input-number
                v-model="loginConfig.maxAttempts"
                :min="3"
                :max="10"
                controls-position="right"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="锁定时间" prop="lockoutDuration">
              <el-input-number
                v-model="loginConfig.lockoutDuration"
                :min="5"
                :max="1440"
                controls-position="right"
              />
              <span class="form-tip">分钟</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会话超时时间" prop="sessionTimeout">
              <el-input-number
                v-model="loginConfig.sessionTimeout"
                :min="30"
                :max="1440"
                controls-position="right"
              />
              <span class="form-tip">分钟</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="记住登录状态" prop="rememberDuration">
              <el-input-number
                v-model="loginConfig.rememberDuration"
                :min="1"
                :max="30"
                controls-position="right"
              />
              <span class="form-tip">天</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="启用验证码">
              <el-switch v-model="loginConfig.enableCaptcha" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="强制HTTPS">
              <el-switch v-model="loginConfig.forceHttps" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单点登录">
              <el-switch v-model="loginConfig.singleSignOn" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- IP白名单 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Connection /></el-icon>
            <span class="header-title">IP访问控制</span>
          </div>
          <div class="header-actions">
            <el-button type="success" @click="handleAddIP">
              <el-icon><Plus /></el-icon>
              添加IP
            </el-button>
          </div>
        </div>
      </template>

      <div class="ip-control-section">
        <el-row :gutter="20" class="control-options">
          <el-col :span="8">
            <el-form-item label="启用IP白名单">
              <el-switch v-model="ipConfig.enableWhitelist" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="启用IP黑名单">
              <el-switch v-model="ipConfig.enableBlacklist" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="记录访问日志">
              <el-switch v-model="ipConfig.logAccess" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- IP列表 -->
        <el-tabs v-model="activeIPTab" class="ip-tabs">
          <el-tab-pane label="白名单" name="whitelist">
            <el-table :data="ipConfig.whitelist" class="ip-table">
              <el-table-column prop="ip" label="IP地址" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="createdAt" label="添加时间" />
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleRemoveIP('whitelist', scope.$index)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="黑名单" name="blacklist">
            <el-table :data="ipConfig.blacklist" class="ip-table">
              <el-table-column prop="ip" label="IP地址" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="createdAt" label="添加时间" />
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleRemoveIP('blacklist', scope.$index)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

    <!-- 安全日志 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Document /></el-icon>
            <span class="header-title">安全日志</span>
          </div>
          <div class="header-actions">
            <el-button type="warning" @click="handleClearLogs">
              <el-icon><Delete /></el-icon>
              清空日志
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="securityLogs" class="security-logs-table">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getLogTypeColor(scope.row.type)" size="small">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ip" label="IP地址" width="150" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="result" label="结果" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.result === '成功' ? 'success' : 'danger'" size="small">
              {{ scope.row.result }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加IP对话框 -->
    <el-dialog v-model="ipDialogVisible" title="添加IP地址" width="500px">
      <el-form :model="ipForm" :rules="ipRules" ref="ipFormRef" label-width="80px">
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="ipForm.type">
            <el-radio value="whitelist">白名单</el-radio>
            <el-radio value="blacklist">黑名单</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="IP地址" prop="ip">
          <el-input v-model="ipForm.ip" placeholder="请输入IP地址，如：192.168.1.1" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="ipForm.description" placeholder="请输入描述信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ipDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmAddIP">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Lock, Check, User, Connection, Document, Delete, Plus
} from '@element-plus/icons-vue'

// 响应式数据
const savePasswordLoading = ref(false)
const saveLoginLoading = ref(false)
const passwordFormRef = ref()
const loginFormRef = ref()
const ipFormRef = ref()
const activeIPTab = ref('whitelist')
const ipDialogVisible = ref(false)

// 密码策略配置
const passwordConfig = reactive({
  minLength: 8,
  expireDays: 90,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: false,
  forbidSequential: true,
  forbidRepeated: true
})

// 登录安全配置
const loginConfig = reactive({
  maxAttempts: 5,
  lockoutDuration: 30,
  sessionTimeout: 120,
  rememberDuration: 7,
  enableCaptcha: true,
  forceHttps: true,
  singleSignOn: false
})

// IP控制配置
const ipConfig = reactive({
  enableWhitelist: false,
  enableBlacklist: true,
  logAccess: true,
  whitelist: [
    { ip: '192.168.1.100', description: '办公室网络', createdAt: '2024-01-15 10:30:00' },
    { ip: '10.0.0.0/8', description: '内网段', createdAt: '2024-01-15 10:31:00' }
  ],
  blacklist: [
    { ip: '192.168.1.200', description: '恶意IP', createdAt: '2024-01-15 11:00:00' }
  ]
})

// IP表单
const ipForm = reactive({
  type: 'whitelist',
  ip: '',
  description: ''
})

// 安全日志
const securityLogs = ref([
  {
    time: '2024-01-15 14:30:25',
    type: '登录尝试',
    ip: '192.168.1.100',
    user: 'admin',
    description: '用户登录',
    result: '成功'
  },
  {
    time: '2024-01-15 14:25:10',
    type: '密码错误',
    ip: '192.168.1.200',
    user: 'test',
    description: '密码错误3次',
    result: '失败'
  },
  {
    time: '2024-01-15 14:20:05',
    type: 'IP拦截',
    ip: '192.168.1.200',
    user: '-',
    description: 'IP在黑名单中',
    result: '拦截'
  }
])

// 表单验证规则
const passwordRules = {
  minLength: [
    { required: true, message: '请设置最小密码长度', trigger: 'blur' }
  ],
  expireDays: [
    { required: true, message: '请设置密码有效期', trigger: 'blur' }
  ]
}

const loginRules = {
  maxAttempts: [
    { required: true, message: '请设置最大登录尝试次数', trigger: 'blur' }
  ],
  lockoutDuration: [
    { required: true, message: '请设置锁定时间', trigger: 'blur' }
  ],
  sessionTimeout: [
    { required: true, message: '请设置会话超时时间', trigger: 'blur' }
  ]
}

const ipRules = {
  ip: [
    { required: true, message: '请输入IP地址', trigger: 'blur' },
    {
      pattern: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\/(?:[0-9]|[1-2][0-9]|3[0-2]))?$/,
      message: '请输入正确的IP地址或CIDR格式',
      trigger: 'blur'
    }
  ],
  description: [
    { required: true, message: '请输入描述信息', trigger: 'blur' }
  ]
}

// 方法
const handleSavePassword = async () => {
  try {
    await passwordFormRef.value?.validate()
    savePasswordLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('密码策略保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    savePasswordLoading.value = false
  }
}

const handleSaveLogin = async () => {
  try {
    await loginFormRef.value?.validate()
    saveLoginLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('登录安全设置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoginLoading.value = false
  }
}

const handleAddIP = () => {
  ipForm.type = activeIPTab.value
  ipForm.ip = ''
  ipForm.description = ''
  ipDialogVisible.value = true
}

const handleConfirmAddIP = async () => {
  try {
    await ipFormRef.value?.validate()

    const newIP = {
      ip: ipForm.ip,
      description: ipForm.description,
      createdAt: new Date().toLocaleString('zh-CN')
    }

    if (ipForm.type === 'whitelist') {
      ipConfig.whitelist.push(newIP)
    } else {
      ipConfig.blacklist.push(newIP)
    }

    ipDialogVisible.value = false
    ElMessage.success('IP地址添加成功')
  } catch (error) {
    console.error('添加失败:', error)
  }
}

const handleRemoveIP = (type, index) => {
  if (type === 'whitelist') {
    ipConfig.whitelist.splice(index, 1)
  } else {
    ipConfig.blacklist.splice(index, 1)
  }
  ElMessage.success('IP地址删除成功')
}

const handleClearLogs = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有安全日志吗？此操作不可撤销！',
      '清空确认',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    securityLogs.value = []
    ElMessage.success('安全日志已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空日志失败:', error)
    }
  }
}

const getLogTypeColor = (type) => {
  const colorMap = {
    '登录尝试': 'info',
    '密码错误': 'warning',
    'IP拦截': 'danger',
    '权限验证': 'success'
  }
  return colorMap[type] || 'info'
}
</script>

<style scoped>
.security-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 卡片样式 */
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

/* 表单样式 */
.el-form-item {
  margin-bottom: 20px;
}

.form-tip {
  margin-left: 8px;
  font-size: 12px;
  color: #909399;
}

.el-input-number {
  width: 100%;
}

/* IP控制区域 */
.ip-control-section {
  margin-top: 16px;
}

.control-options {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.ip-tabs {
  margin-top: 20px;
}

.ip-table {
  margin-top: 16px;
}

/* 安全日志表格 */
.security-logs-table {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .security-settings {
    gap: 16px;
  }

  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .control-options {
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .header-actions {
    flex-direction: column;
    gap: 8px;
  }

  .header-actions .el-button {
    width: 100%;
  }
}
</style>
