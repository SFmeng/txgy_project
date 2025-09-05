<template>
  <div class="backup-settings">
    <!-- 备份配置 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Download /></el-icon>
            <span class="header-title">备份配置</span>
          </div>
          <div class="header-actions">
            <el-button type="success" @click="handleBackupNow" :loading="backupLoading">
              <el-icon><Download /></el-icon>
              立即备份
            </el-button>
            <el-button type="primary" @click="handleSave" :loading="saveLoading">
              <el-icon><Check /></el-icon>
              保存配置
            </el-button>
          </div>
        </div>
      </template>

      <el-form :model="backupConfig" :rules="backupRules" ref="backupFormRef" label-width="120px">
        <div class="form-section">
          <h4 class="section-subtitle">自动备份设置</h4>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="启用自动备份">
                <el-switch v-model="backupConfig.autoBackup" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="备份频率" prop="frequency">
                <el-select v-model="backupConfig.frequency" placeholder="请选择备份频率">
                  <el-option label="每天" value="daily" />
                  <el-option label="每周" value="weekly" />
                  <el-option label="每月" value="monthly" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="备份时间" prop="backupTime">
                <el-time-picker
                  v-model="backupConfig.backupTime"
                  format="HH:mm"
                  placeholder="选择备份时间"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h4 class="section-subtitle">备份内容</h4>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="数据库">
                <el-switch v-model="backupConfig.includeDatabase" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="用户文件">
                <el-switch v-model="backupConfig.includeFiles" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="系统配置">
                <el-switch v-model="backupConfig.includeConfig" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="日志文件">
                <el-switch v-model="backupConfig.includeLogs" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h4 class="section-subtitle">备份保留</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="保留份数" prop="retentionCount">
                <el-input-number
                  v-model="backupConfig.retentionCount"
                  :min="1"
                  :max="30"
                  controls-position="right"
                />
                <span class="form-tip">份</span>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="压缩备份">
                <el-switch v-model="backupConfig.compress" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
    </el-card>

    <!-- 备份记录 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><List /></el-icon>
            <span class="header-title">备份记录</span>
          </div>
          <div class="header-actions">
            <el-button type="warning" @click="handleClearBackups">
              <el-icon><Delete /></el-icon>
              清理备份
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="backupRecords" class="backup-table">
        <el-table-column prop="name" label="备份文件名" />
        <el-table-column prop="size" label="文件大小" width="120" />
        <el-table-column prop="type" label="备份类型" width="120">
          <template #default="scope">
            <el-tag :type="getBackupTypeColor(scope.row.type)" size="small">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '成功' ? 'success' : 'danger'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" type="primary" @click="handleDownload(scope.row)">
              下载
            </el-button>
            <el-button size="small" type="warning" @click="handleRestore(scope.row)">
              恢复
            </el-button>
            <el-button size="small" type="danger" @click="handleDeleteBackup(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 恢复操作 -->
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Upload /></el-icon>
            <span class="header-title">恢复操作</span>
          </div>
        </div>
      </template>

      <div class="restore-section">
        <el-alert
          title="注意事项"
          type="warning"
          description="恢复操作将覆盖当前数据，请确保在安全的环境下进行操作，建议先进行当前数据的备份。"
          show-icon
          :closable="false"
        />

        <div class="restore-upload">
          <el-upload
            class="upload-demo"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="uploadFileList"
            accept=".zip,.sql,.tar.gz"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将备份文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 .zip, .sql, .tar.gz 格式的备份文件
              </div>
            </template>
          </el-upload>

          <div class="restore-actions">
            <el-button type="danger" @click="handleRestoreFromFile" :loading="restoreLoading" :disabled="!uploadFileList.length">
              <el-icon><Upload /></el-icon>
              开始恢复
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Download, Check, List, Delete, Upload, UploadFilled
} from '@element-plus/icons-vue'

// 响应式数据
const saveLoading = ref(false)
const backupLoading = ref(false)
const restoreLoading = ref(false)
const backupFormRef = ref()
const uploadFileList = ref([])

// 备份配置
const backupConfig = reactive({
  autoBackup: true,
  frequency: 'daily',
  backupTime: new Date(2024, 0, 1, 2, 0), // 凌晨2点
  includeDatabase: true,
  includeFiles: true,
  includeConfig: true,
  includeLogs: false,
  retentionCount: 7,
  compress: true
})

// 备份记录
const backupRecords = ref([
  {
    name: 'backup_20240115_020000.zip',
    size: '125.6MB',
    type: '完整备份',
    createTime: '2024-01-15 02:00:00',
    status: '成功'
  },
  {
    name: 'backup_20240114_020000.zip',
    size: '123.2MB',
    type: '完整备份',
    createTime: '2024-01-14 02:00:00',
    status: '成功'
  },
  {
    name: 'backup_20240113_020000.zip',
    size: '121.8MB',
    type: '完整备份',
    createTime: '2024-01-13 02:00:00',
    status: '失败'
  }
])

// 表单验证规则
const backupRules = {
  frequency: [
    { required: true, message: '请选择备份频率', trigger: 'change' }
  ],
  retentionCount: [
    { required: true, message: '请设置保留份数', trigger: 'blur' }
  ]
}

// 方法
const handleSave = async () => {
  try {
    await backupFormRef.value?.validate()
    saveLoading.value = true

    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('备份配置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('保存失败')
    }
  } finally {
    saveLoading.value = false
  }
}

const handleBackupNow = async () => {
  try {
    backupLoading.value = true

    // 模拟备份过程
    await new Promise(resolve => setTimeout(resolve, 3000))

    // 添加新的备份记录
    const now = new Date()
    const backupName = `backup_${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}_${now.getHours().toString().padStart(2, '0')}${now.getMinutes().toString().padStart(2, '0')}${now.getSeconds().toString().padStart(2, '0')}.zip`

    backupRecords.value.unshift({
      name: backupName,
      size: '126.8MB',
      type: '手动备份',
      createTime: now.toLocaleString('zh-CN'),
      status: '成功'
    })

    ElMessage.success('备份创建成功')
  } catch (error) {
    console.error('备份失败:', error)
    ElMessage.error('备份创建失败')
  } finally {
    backupLoading.value = false
  }
}

const handleDownload = (backup) => {
  // 模拟下载
  ElMessage.success(`开始下载 ${backup.name}`)
}

const handleRestore = async (backup) => {
  try {
    await ElMessageBox.confirm(
      `确定要从备份"${backup.name}"恢复数据吗？此操作将覆盖当前所有数据！`,
      '恢复确认',
      {
        confirmButtonText: '确定恢复',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 模拟恢复过程
    await new Promise(resolve => setTimeout(resolve, 5000))

    ElMessage.success('数据恢复成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('恢复失败:', error)
      ElMessage.error('数据恢复失败')
    }
  }
}

const handleDeleteBackup = async (backup) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除备份"${backup.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const index = backupRecords.value.findIndex(b => b.name === backup.name)
    if (index > -1) {
      backupRecords.value.splice(index, 1)
      ElMessage.success('备份删除成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const handleClearBackups = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清理所有备份文件吗？此操作不可撤销！',
      '清理确认',
      {
        confirmButtonText: '确定清理',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    backupRecords.value = []
    ElMessage.success('备份文件已清理')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清理失败:', error)
    }
  }
}

const handleFileChange = (file) => {
  uploadFileList.value = [file]
}

const handleRestoreFromFile = async () => {
  try {
    if (!uploadFileList.value.length) {
      ElMessage.warning('请先选择备份文件')
      return
    }

    await ElMessageBox.confirm(
      '确定要从上传的文件恢复数据吗？此操作将覆盖当前所有数据！',
      '恢复确认',
      {
        confirmButtonText: '确定恢复',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    restoreLoading.value = true

    // 模拟恢复过程
    await new Promise(resolve => setTimeout(resolve, 5000))

    uploadFileList.value = []
    ElMessage.success('从文件恢复成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('恢复失败:', error)
      ElMessage.error('从文件恢复失败')
    }
  } finally {
    restoreLoading.value = false
  }
}

const getBackupTypeColor = (type) => {
  const colorMap = {
    '完整备份': 'success',
    '增量备份': 'warning',
    '手动备份': 'info'
  }
  return colorMap[type] || 'info'
}
</script>

<style scoped>
.backup-settings {
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

.backup-table {
  margin-top: 16px;
}

.restore-section {
  padding: 16px 0;
}

.restore-upload {
  margin-top: 20px;
}

.restore-actions {
  margin-top: 16px;
  text-align: center;
}

.upload-demo {
  width: 100%;
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
