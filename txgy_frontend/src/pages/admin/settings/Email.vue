<template>
  <div class="email-settings">
    <!-- SMTP配置 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Message /></el-icon>
            <span class="header-title">SMTP邮件配置</span>
          </div>
          <div class="header-actions">
            <el-button type="success" @click="handleTestEmail" :loading="testLoading">
              <el-icon><Connection /></el-icon>
              测试连接
            </el-button>
            <el-button type="primary" @click="handleSave" :loading="saveLoading">
              <el-icon><Check /></el-icon>
              保存配置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="emailConfig" :rules="emailRules" ref="emailFormRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="SMTP服务器" prop="host">
              <el-input v-model="emailConfig.host" placeholder="如：smtp.qq.com">
                <template #prefix>
                  <el-icon><Connection /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="端口号" prop="port">
              <el-input-number v-model="emailConfig.port" :min="1" :max="65535" controls-position="right" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发件人邮箱" prop="username">
              <el-input v-model="emailConfig.username" placeholder="请输入发件人邮箱">
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱密码" prop="password">
              <el-input v-model="emailConfig.password" type="password" show-password placeholder="请输入邮箱密码或授权码">
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发件人名称" prop="fromName">
              <el-input v-model="emailConfig.fromName" placeholder="请输入发件人名称">
                <template #prefix>
                  <el-icon><UserFilled /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="加密方式" prop="encryption">
              <el-select v-model="emailConfig.encryption" placeholder="请选择加密方式">
                <el-option label="无加密" value="none" />
                <el-option label="SSL" value="ssl" />
                <el-option label="TLS" value="tls" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="启用邮件服务">
              <el-switch v-model="emailConfig.enabled" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="启用调试模式">
              <el-switch v-model="emailConfig.debug" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="验证SSL证书">
              <el-switch v-model="emailConfig.verifySSL" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 邮件模板 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Document /></el-icon>
            <span class="header-title">邮件模板</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleSaveTemplate" :loading="saveTemplateLoading">
              <el-icon><Check /></el-icon>
              保存模板
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTemplateTab" class="template-tabs">
        <el-tab-pane label="用户注册" name="register">
          <el-form :model="templates.register" label-width="100px">
            <el-form-item label="邮件主题">
              <el-input v-model="templates.register.subject" placeholder="请输入邮件主题" />
            </el-form-item>
            <el-form-item label="邮件内容">
              <el-input
                v-model="templates.register.content"
                type="textarea"
                :rows="8"
                placeholder="请输入邮件内容，支持HTML格式"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="密码重置" name="reset">
          <el-form :model="templates.reset" label-width="100px">
            <el-form-item label="邮件主题">
              <el-input v-model="templates.reset.subject" placeholder="请输入邮件主题" />
            </el-form-item>
            <el-form-item label="邮件内容">
              <el-input
                v-model="templates.reset.content"
                type="textarea"
                :rows="8"
                placeholder="请输入邮件内容，支持HTML格式"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="系统通知" name="notification">
          <el-form :model="templates.notification" label-width="100px">
            <el-form-item label="邮件主题">
              <el-input v-model="templates.notification.subject" placeholder="请输入邮件主题" />
            </el-form-item>
            <el-form-item label="邮件内容">
              <el-input
                v-model="templates.notification.content"
                type="textarea"
                :rows="8"
                placeholder="请输入邮件内容，支持HTML格式"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <div class="template-variables">
        <h4>可用变量：</h4>
        <el-tag v-for="variable in templateVariables" :key="variable" size="small" class="variable-tag">
          {{ variable }}
        </el-tag>
      </div>
    </el-card>

    <!-- 邮件发送记录 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><List /></el-icon>
            <span class="header-title">邮件发送记录</span>
          </div>
          <div class="header-actions">
            <el-button type="warning" @click="handleClearLogs">
              <el-icon><Delete /></el-icon>
              清空记录
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="emailLogs" class="email-logs-table">
        <el-table-column prop="time" label="发送时间" width="180" />
        <el-table-column prop="to" label="收件人" width="200" />
        <el-table-column prop="subject" label="邮件主题" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getEmailTypeColor(scope.row.type)" size="small">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '成功' ? 'success' : 'danger'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Message, Connection, Check, User, Lock, UserFilled, Document, List, Delete
} from '@element-plus/icons-vue'

// 响应式数据
const saveLoading = ref(false)
const testLoading = ref(false)
const saveTemplateLoading = ref(false)
const emailFormRef = ref()
const activeTemplateTab = ref('register')

// 邮件配置
const emailConfig = reactive({
  host: 'smtp.qq.com',
  port: 587,
  username: 'admin@company.com',
  password: '',
  fromName: '企业管理系统',
  encryption: 'tls',
  enabled: true,
  debug: false,
  verifySSL: true
})

// 邮件模板
const templates = reactive({
  register: {
    subject: '欢迎注册企业管理系统',
    content: `<h2>欢迎注册</h2>
<p>亲爱的 {{username}}，</p>
<p>感谢您注册我们的企业管理系统！</p>
<p>请点击以下链接激活您的账户：</p>
<p><a href="{{activation_link}}">激活账户</a></p>
<p>如果您没有注册此账户，请忽略此邮件。</p>`
  },
  reset: {
    subject: '密码重置请求',
    content: `<h2>密码重置</h2>
<p>亲爱的 {{username}}，</p>
<p>您请求重置密码。请点击以下链接重置您的密码：</p>
<p><a href="{{reset_link}}">重置密码</a></p>
<p>此链接将在24小时后失效。</p>`
  },
  notification: {
    subject: '系统通知',
    content: `<h2>系统通知</h2>
<p>亲爱的 {{username}}，</p>
<p>{{notification_content}}</p>
<p>感谢您使用我们的服务！</p>`
  }
})

// 模板变量
const templateVariables = [
  '{{username}}', '{{email}}', '{{activation_link}}', '{{reset_link}}', 
  '{{notification_content}}', '{{site_name}}', '{{current_time}}'
]

// 邮件发送记录
const emailLogs = ref([
  {
    time: '2024-01-15 14:30:25',
    to: 'user@example.com',
    subject: '欢迎注册企业管理系统',
    type: '注册确认',
    status: '成功'
  },
  {
    time: '2024-01-15 14:25:10',
    to: 'test@example.com',
    subject: '密码重置请求',
    type: '密码重置',
    status: '失败'
  }
])

// 表单验证规则
const emailRules = {
  host: [
    { required: true, message: '请输入SMTP服务器地址', trigger: 'blur' }
  ],
  port: [
    { required: true, message: '请输入端口号', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入发件人邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入邮箱密码', trigger: 'blur' }
  ],
  fromName: [
    { required: true, message: '请输入发件人名称', trigger: 'blur' }
  ]
}

// 方法
const handleSave = async () => {
  try {
    await emailFormRef.value?.validate()
    saveLoading.value = true
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('邮件配置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoading.value = false
  }
}

const handleTestEmail = async () => {
  try {
    testLoading.value = true
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    ElMessage.success('邮件连接测试成功')
  } catch (error) {
    console.error('测试失败:', error)
    ElMessage.error('邮件连接测试失败')
  } finally {
    testLoading.value = false
  }
}

const handleSaveTemplate = async () => {
  try {
    saveTemplateLoading.value = true
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('邮件模板保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saveTemplateLoading.value = false
  }
}

const handleClearLogs = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有邮件发送记录吗？',
      '清空确认',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    emailLogs.value = []
    ElMessage.success('邮件记录已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空记录失败:', error)
    }
  }
}

const getEmailTypeColor = (type) => {
  const colorMap = {
    '注册确认': 'success',
    '密码重置': 'warning',
    '系统通知': 'info'
  }
  return colorMap[type] || 'info'
}
</script>

<style scoped>
.email-settings {
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

.template-tabs {
  margin-top: 16px;
}

.template-variables {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.template-variables h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.variable-tag {
  margin: 4px 8px 4px 0;
}

.email-logs-table {
  margin-top: 16px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
