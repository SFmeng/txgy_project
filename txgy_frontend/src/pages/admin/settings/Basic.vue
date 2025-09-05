<template>
  <div class="basic-settings">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Tools /></el-icon>
            <span class="header-title">基础配置</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleSave" :loading="saveLoading">
              <el-icon><Check /></el-icon>
              保存配置
            </el-button>
            <el-button @click="handleReset">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="basicConfig" :rules="basicRules" ref="basicFormRef" label-width="120px">
        <!-- 网站基本信息 -->
        <div class="form-section">
          <h3 class="section-title">网站基本信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="网站名称" prop="siteName">
                <el-input v-model="basicConfig.siteName" placeholder="请输入网站名称">
                  <template #prefix>
                    <el-icon><House /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="网站标题" prop="siteTitle">
                <el-input v-model="basicConfig.siteTitle" placeholder="请输入网站标题">
                  <template #prefix>
                    <el-icon><Document /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="网站描述" prop="siteDescription">
            <el-input
              v-model="basicConfig.siteDescription"
              type="textarea"
              :rows="3"
              placeholder="请输入网站描述"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="网站关键词" prop="siteKeywords">
                <el-input v-model="basicConfig.siteKeywords" placeholder="请输入关键词，用逗号分隔">
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="网站版本" prop="version">
                <el-input v-model="basicConfig.version" placeholder="请输入版本号">
                  <template #prefix>
                    <el-icon><Flag /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 联系信息 -->
        <div class="form-section">
          <h3 class="section-title">联系信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="联系邮箱" prop="contactEmail">
                <el-input v-model="basicConfig.contactEmail" placeholder="请输入联系邮箱">
                  <template #prefix>
                    <el-icon><Message /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系电话" prop="contactPhone">
                <el-input v-model="basicConfig.contactPhone" placeholder="请输入联系电话">
                  <template #prefix>
                    <el-icon><Phone /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="公司地址" prop="companyAddress">
            <el-input v-model="basicConfig.companyAddress" placeholder="请输入公司地址">
              <template #prefix>
                <el-icon><Location /></el-icon>
              </template>
            </el-input>
          </el-form-item>
        </div>

        <!-- 系统设置 -->
        <div class="form-section">
          <h3 class="section-title">系统设置</h3>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="用户注册">
                <el-switch
                  v-model="basicConfig.allowRegister"
                  active-text="允许"
                  inactive-text="禁止"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="邮箱验证">
                <el-switch
                  v-model="basicConfig.requireEmailVerify"
                  active-text="必须"
                  inactive-text="可选"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="维护模式">
                <el-switch
                  v-model="basicConfig.maintenanceMode"
                  active-text="开启"
                  inactive-text="关闭"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="默认语言" prop="defaultLanguage">
                <el-select v-model="basicConfig.defaultLanguage" placeholder="请选择默认语言">
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                  <el-option label="繁體中文" value="zh-TW" />
                  <el-option label="日本語" value="ja-JP" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="时区设置" prop="timezone">
                <el-select v-model="basicConfig.timezone" placeholder="请选择时区">
                  <el-option label="北京时间 (UTC+8)" value="Asia/Shanghai" />
                  <el-option label="东京时间 (UTC+9)" value="Asia/Tokyo" />
                  <el-option label="纽约时间 (UTC-5)" value="America/New_York" />
                  <el-option label="伦敦时间 (UTC+0)" value="Europe/London" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 上传设置 -->
        <div class="form-section">
          <h3 class="section-title">上传设置</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="最大文件大小" prop="maxFileSize">
                <el-input v-model="basicConfig.maxFileSize" placeholder="请输入最大文件大小">
                  <template #append>MB</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="允许的文件类型" prop="allowedFileTypes">
                <el-input v-model="basicConfig.allowedFileTypes" placeholder="如：jpg,png,pdf">
                  <template #prefix>
                    <el-icon><Files /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 缓存设置 -->
        <div class="form-section">
          <h3 class="section-title">缓存设置</h3>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="启用缓存">
                <el-switch
                  v-model="basicConfig.enableCache"
                  active-text="启用"
                  inactive-text="禁用"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="缓存时间" prop="cacheTime">
                <el-input v-model="basicConfig.cacheTime" placeholder="缓存时间">
                  <template #append>分钟</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-button type="warning" @click="handleClearCache" :loading="clearCacheLoading">
                  <el-icon><Delete /></el-icon>
                  清除缓存
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <!-- 系统信息卡片 -->
    <el-card class="system-info-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Monitor /></el-icon>
            <span class="header-title">系统信息</span>
          </div>
        </div>
      </template>

      <div class="system-info-grid">
        <div class="info-item">
          <div class="info-label">服务器时间</div>
          <div class="info-value">{{ currentTime }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">系统版本</div>
          <div class="info-value">{{ systemInfo.version }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">PHP版本</div>
          <div class="info-value">{{ systemInfo.phpVersion }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">数据库版本</div>
          <div class="info-value">{{ systemInfo.dbVersion }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">运行时间</div>
          <div class="info-value">{{ systemInfo.uptime }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">磁盘使用</div>
          <div class="info-value">{{ systemInfo.diskUsage }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Tools, Check, RefreshLeft, House, Document, Key, Flag, Message, Phone, Location,
  Files, Delete, Monitor
} from '@element-plus/icons-vue'

// 响应式数据
const saveLoading = ref(false)
const clearCacheLoading = ref(false)
const basicFormRef = ref()
const currentTime = ref('')

// 基础配置数据
const basicConfig = reactive({
  siteName: '企业管理系统',
  siteTitle: '高效企业管理平台',
  siteDescription: '专业的企业管理解决方案，提供用户管理、权限控制、数据分析等功能',
  siteKeywords: '企业管理,用户管理,权限系统,数据分析',
  version: '1.0.0',
  contactEmail: 'admin@company.com',
  contactPhone: '400-123-4567',
  companyAddress: '北京市朝阳区科技园区创新大厦',
  allowRegister: true,
  requireEmailVerify: true,
  maintenanceMode: false,
  defaultLanguage: 'zh-CN',
  timezone: 'Asia/Shanghai',
  maxFileSize: '10',
  allowedFileTypes: 'jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx',
  enableCache: true,
  cacheTime: '60'
})

// 系统信息
const systemInfo = reactive({
  version: 'v1.0.0',
  phpVersion: 'PHP 8.1.0',
  dbVersion: 'MySQL 8.0.28',
  uptime: '15天 8小时 32分钟',
  diskUsage: '45.2GB / 100GB (45%)'
})

// 表单验证规则
const basicRules = {
  siteName: [
    { required: true, message: '请输入网站名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  siteTitle: [
    { required: true, message: '请输入网站标题', trigger: 'blur' }
  ],
  contactEmail: [
    { required: true, message: '请输入联系邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  contactPhone: [
    { pattern: /^1[3-9]\d{9}$|^400-\d{3}-\d{4}$/, message: '请输入正确的电话号码', trigger: 'blur' }
  ],
  maxFileSize: [
    { required: true, message: '请输入最大文件大小', trigger: 'blur' },
    { pattern: /^\d+$/, message: '请输入数字', trigger: 'blur' }
  ],
  cacheTime: [
    { pattern: /^\d+$/, message: '请输入数字', trigger: 'blur' }
  ]
}

// 方法
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const handleSave = async () => {
  try {
    await basicFormRef.value?.validate()
    saveLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1500))

    ElMessage.success('基础配置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) { // 表单验证失败时error为false
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoading.value = false
  }
}

const handleReset = () => {
  basicFormRef.value?.resetFields()
  ElMessage.info('配置已重置')
}

const handleClearCache = async () => {
  try {
    clearCacheLoading.value = true

    // 模拟清除缓存
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('缓存清除成功')
  } catch (error) {
    console.error('清除缓存失败:', error)
    ElMessage.error('清除缓存失败')
  } finally {
    clearCacheLoading.value = false
  }
}

// 定时器
let timeInterval = null

// 生命周期
onMounted(() => {
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.basic-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 卡片样式 */
.settings-card, .system-info-card {
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

/* 表单区域 */
.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
  padding-left: 12px;
  border-left: 4px solid #409eff;
}

/* 表单项样式 */
.el-form-item {
  margin-bottom: 20px;
}

.el-input, .el-select, .el-textarea {
  width: 100%;
}

.el-switch {
  --el-switch-on-color: #409eff;
}

/* 系统信息网格 */
.system-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.info-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: #303133;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .system-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .basic-settings {
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

  .form-section {
    margin-bottom: 24px;
    padding-bottom: 16px;
  }

  .section-title {
    font-size: 14px;
    margin-bottom: 16px;
  }

  .system-info-grid {
    grid-template-columns: 1fr;
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
