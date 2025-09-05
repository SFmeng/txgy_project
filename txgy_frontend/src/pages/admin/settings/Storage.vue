<template>
  <div class="storage-settings">
    <!-- 存储配置 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><FolderOpened /></el-icon>
            <span class="header-title">存储配置</span>
          </div>
          <div class="header-actions">
            <el-button type="success" @click="handleTestStorage" :loading="testLoading">
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

      <el-form :model="storageConfig" :rules="storageRules" ref="storageFormRef" label-width="120px">
        <el-form-item label="存储类型" prop="type">
          <el-radio-group v-model="storageConfig.type">
            <el-radio value="local">本地存储</el-radio>
            <el-radio value="oss">阿里云OSS</el-radio>
            <el-radio value="cos">腾讯云COS</el-radio>
            <el-radio value="s3">Amazon S3</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 本地存储配置 -->
        <div v-if="storageConfig.type === 'local'" class="storage-section">
          <h4 class="section-subtitle">本地存储配置</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="存储路径" prop="localPath">
                <el-input v-model="storageConfig.localPath" placeholder="如：/var/www/uploads">
                  <template #prefix>
                    <el-icon><Folder /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="访问URL前缀" prop="localUrl">
                <el-input v-model="storageConfig.localUrl" placeholder="如：https://example.com/uploads">
                  <template #prefix>
                    <el-icon><Link /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 云存储配置 -->
        <div v-if="storageConfig.type !== 'local'" class="storage-section">
          <h4 class="section-subtitle">云存储配置</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Access Key" prop="accessKey">
                <el-input v-model="storageConfig.accessKey" placeholder="请输入Access Key">
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Secret Key" prop="secretKey">
                <el-input v-model="storageConfig.secretKey" type="password" show-password placeholder="请输入Secret Key">
                  <template #prefix>
                    <el-icon><Lock /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="存储桶名称" prop="bucket">
                <el-input v-model="storageConfig.bucket" placeholder="请输入存储桶名称">
                  <template #prefix>
                    <el-icon><Box /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="地域" prop="region">
                <el-select v-model="storageConfig.region" placeholder="请选择地域">
                  <el-option label="华北1（青岛）" value="cn-qingdao" />
                  <el-option label="华北2（北京）" value="cn-beijing" />
                  <el-option label="华东1（杭州）" value="cn-hangzhou" />
                  <el-option label="华东2（上海）" value="cn-shanghai" />
                  <el-option label="华南1（深圳）" value="cn-shenzhen" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="自定义域名" prop="customDomain">
            <el-input v-model="storageConfig.customDomain" placeholder="请输入自定义域名（可选）">
              <template #prefix>
                <el-icon><Globe /></el-icon>
              </template>
            </el-input>
          </el-form-item>
        </div>

        <!-- 通用配置 -->
        <div class="storage-section">
          <h4 class="section-subtitle">通用配置</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="最大文件大小" prop="maxFileSize">
                <el-input-number
                  v-model="storageConfig.maxFileSize"
                  :min="1"
                  :max="1024"
                  controls-position="right"
                />
                <span class="form-tip">MB</span>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="允许的文件类型" prop="allowedTypes">
                <el-input v-model="storageConfig.allowedTypes" placeholder="如：jpg,png,pdf">
                  <template #prefix>
                    <el-icon><Files /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="启用缩略图">
                <el-switch v-model="storageConfig.enableThumbnail" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="启用水印">
                <el-switch v-model="storageConfig.enableWatermark" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="自动清理">
                <el-switch v-model="storageConfig.autoCleanup" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <!-- 存储统计 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><DataBoard /></el-icon>
            <span class="header-title">存储统计</span>
          </div>
          <div class="header-actions">
            <el-button type="warning" @click="handleCleanup">
              <el-icon><Delete /></el-icon>
              清理垃圾文件
            </el-button>
          </div>
        </div>
      </template>

      <div class="storage-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon total">
                <el-icon><FolderOpened /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ storageStats.totalSize }}</div>
                <div class="stat-label">总存储空间</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon used">
                <el-icon><Files /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ storageStats.usedSize }}</div>
                <div class="stat-label">已使用空间</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon files">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ storageStats.fileCount }}</div>
                <div class="stat-label">文件数量</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon temp">
                <el-icon><Delete /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ storageStats.tempSize }}</div>
                <div class="stat-label">临时文件</div>
              </div>
            </div>
          </el-col>
        </el-row>

        <!-- 使用率进度条 -->
        <div class="usage-progress">
          <div class="progress-header">
            <span>存储使用率</span>
            <span>{{ storageStats.usagePercent }}%</span>
          </div>
          <el-progress 
            :percentage="storageStats.usagePercent" 
            :color="getProgressColor(storageStats.usagePercent)"
            :stroke-width="8"
          />
        </div>
      </div>
    </el-card>

    <!-- 文件管理 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Files /></el-icon>
            <span class="header-title">文件管理</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="handleRefreshFiles">
              <el-icon><Refresh /></el-icon>
              刷新列表
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="recentFiles" class="files-table">
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="120" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag size="small">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="uploadTime" label="上传时间" width="180" />
        <el-table-column prop="uploader" label="上传者" width="120" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" type="danger" @click="handleDeleteFile(scope.row)">
              删除
            </el-button>
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
  FolderOpened, Connection, Check, Folder, Link, Key, Lock, Box, Globe,
  DataBoard, Files, Document, Delete, Refresh
} from '@element-plus/icons-vue'

// 响应式数据
const saveLoading = ref(false)
const testLoading = ref(false)
const storageFormRef = ref()

// 存储配置
const storageConfig = reactive({
  type: 'local',
  localPath: '/var/www/uploads',
  localUrl: 'https://example.com/uploads',
  accessKey: '',
  secretKey: '',
  bucket: '',
  region: 'cn-beijing',
  customDomain: '',
  maxFileSize: 10,
  allowedTypes: 'jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx,zip',
  enableThumbnail: true,
  enableWatermark: false,
  autoCleanup: true
})

// 存储统计
const storageStats = reactive({
  totalSize: '100GB',
  usedSize: '45.2GB',
  fileCount: '12,456',
  tempSize: '2.1GB',
  usagePercent: 45
})

// 最近文件
const recentFiles = ref([
  {
    name: 'document.pdf',
    size: '2.5MB',
    type: 'PDF',
    uploadTime: '2024-01-15 14:30:25',
    uploader: 'admin'
  },
  {
    name: 'image.jpg',
    size: '1.2MB',
    type: 'JPG',
    uploadTime: '2024-01-15 14:25:10',
    uploader: 'user1'
  },
  {
    name: 'report.xlsx',
    size: '856KB',
    type: 'XLSX',
    uploadTime: '2024-01-15 14:20:05',
    uploader: 'admin'
  }
])

// 表单验证规则
const storageRules = {
  localPath: [
    { required: true, message: '请输入存储路径', trigger: 'blur' }
  ],
  localUrl: [
    { required: true, message: '请输入访问URL前缀', trigger: 'blur' }
  ],
  accessKey: [
    { required: true, message: '请输入Access Key', trigger: 'blur' }
  ],
  secretKey: [
    { required: true, message: '请输入Secret Key', trigger: 'blur' }
  ],
  bucket: [
    { required: true, message: '请输入存储桶名称', trigger: 'blur' }
  ]
}

// 方法
const handleSave = async () => {
  try {
    await storageFormRef.value?.validate()
    saveLoading.value = true

    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('存储配置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoading.value = false
  }
}

const handleTestStorage = async () => {
  try {
    testLoading.value = true

    await new Promise(resolve => setTimeout(resolve, 2000))

    ElMessage.success('存储连接测试成功')
  } catch (error) {
    console.error('测试失败:', error)
    ElMessage.error('存储连接测试失败')
  } finally {
    testLoading.value = false
  }
}

const handleCleanup = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清理垃圾文件吗？这将删除所有临时文件和无效引用。',
      '清理确认',
      {
        confirmButtonText: '确定清理',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟清理过程
    await new Promise(resolve => setTimeout(resolve, 2000))

    storageStats.tempSize = '0MB'
    ElMessage.success('垃圾文件清理完成')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清理失败:', error)
    }
  }
}

const handleRefreshFiles = () => {
  ElMessage.success('文件列表已刷新')
}

const handleDeleteFile = async (file) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件"${file.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const index = recentFiles.value.findIndex(f => f.name === file.name)
    if (index > -1) {
      recentFiles.value.splice(index, 1)
      ElMessage.success('文件删除成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const getProgressColor = (percentage) => {
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}
</script>

<style scoped>
.storage-settings {
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

.storage-section {
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

/* 存储统计 */
.storage-stats {
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

.stat-icon.total { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.used { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-icon.files { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-icon.temp { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }

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

.usage-progress {
  margin-top: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #303133;
}

.files-table {
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

  .storage-stats .el-row {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
