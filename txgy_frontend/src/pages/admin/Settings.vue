<template>
  <div class="settings-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><Setting /></el-icon>
            系统设置
          </h1>
          <p class="page-description">配置和管理系统的各项参数设置</p>
        </div>
        <div class="header-actions">
          <el-button type="success" @click="handleSaveAll" :loading="saveAllLoading">
            <el-icon><Check /></el-icon>
            保存所有设置
          </el-button>
          <el-button type="warning" @click="handleResetAll">
            <el-icon><RefreshLeft /></el-icon>
            重置为默认
          </el-button>
        </div>
      </div>
    </div>

    <!-- 设置导航和内容 -->
    <el-row :gutter="20">
      <!-- 左侧导航菜单 -->
      <el-col :span="5">
        <el-card class="settings-nav-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Menu /></el-icon>
              <span class="nav-title">设置分类</span>
            </div>
          </template>
          <el-menu
            :default-active="currentSettingPath"
            class="settings-nav"
            @select="handleNavSelect"
          >
            <el-menu-item index="/admin/settings/basic">
              <el-icon><Tools /></el-icon>
              <span>基础配置</span>
            </el-menu-item>
            <el-menu-item index="/admin/settings/security">
              <el-icon><Lock /></el-icon>
              <span>安全设置</span>
            </el-menu-item>
            <el-menu-item index="/admin/settings/email">
              <el-icon><Message /></el-icon>
              <span>邮件配置</span>
            </el-menu-item>
            <el-menu-item index="/admin/settings/storage">
              <el-icon><FolderOpened /></el-icon>
              <span>存储配置</span>
            </el-menu-item>
            <el-menu-item index="/admin/settings/logs">
              <el-icon><Document /></el-icon>
              <span>日志配置</span>
            </el-menu-item>
            <el-menu-item index="/admin/settings/backup">
              <el-icon><Download /></el-icon>
              <span>备份恢复</span>
            </el-menu-item>
          </el-menu>
        </el-card>

        <!-- 设置状态卡片 -->
        <el-card class="settings-status-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Monitor /></el-icon>
              <span class="nav-title">配置状态</span>
            </div>
          </template>
          <div class="status-list">
            <div class="status-item">
              <div class="status-label">基础配置</div>
              <el-tag :type="settingsStatus.basic ? 'success' : 'warning'" size="small">
                {{ settingsStatus.basic ? '已配置' : '待配置' }}
              </el-tag>
            </div>
            <div class="status-item">
              <div class="status-label">安全设置</div>
              <el-tag :type="settingsStatus.security ? 'success' : 'warning'" size="small">
                {{ settingsStatus.security ? '已配置' : '待配置' }}
              </el-tag>
            </div>
            <div class="status-item">
              <div class="status-label">邮件服务</div>
              <el-tag :type="settingsStatus.email ? 'success' : 'warning'" size="small">
                {{ settingsStatus.email ? '已配置' : '待配置' }}
              </el-tag>
            </div>
            <div class="status-item">
              <div class="status-label">存储服务</div>
              <el-tag :type="settingsStatus.storage ? 'success' : 'warning'" size="small">
                {{ settingsStatus.storage ? '已配置' : '待配置' }}
              </el-tag>
            </div>
          </div>
        </el-card>

        <!-- 快速操作 -->
        <el-card class="quick-operations-card">
          <template #header>
            <div class="nav-header">
              <el-icon class="nav-icon"><Lightning /></el-icon>
              <span class="nav-title">快速操作</span>
            </div>
          </template>
          <div class="quick-operations">
            <el-button type="primary" size="small" @click="handleTestConnection" :loading="testLoading">
              <el-icon><Connection /></el-icon>
              测试连接
            </el-button>
            <el-button type="success" size="small" @click="handleExportConfig">
              <el-icon><Upload /></el-icon>
              导出配置
            </el-button>
            <el-button type="warning" size="small" @click="handleImportConfig">
              <el-icon><Download /></el-icon>
              导入配置
            </el-button>
            <el-button type="info" size="small" @click="handleViewLogs">
              <el-icon><View /></el-icon>
              查看日志
            </el-button>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧设置内容 -->
      <el-col :span="19">
        <div class="settings-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting, Check, RefreshLeft, Menu, Tools, Lock, Message, FolderOpened,
  Document, Download, Monitor, Lightning, Connection, Upload, View
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 响应式数据
const saveAllLoading = ref(false)
const testLoading = ref(false)

// 当前设置路径
const currentSettingPath = computed(() => route.path)

// 设置状态
const settingsStatus = ref({
  basic: true,
  security: false,
  email: true,
  storage: false,
  logs: true,
  backup: false
})

// 方法
const handleNavSelect = (path) => {
  router.push(path)
}

const handleSaveAll = async () => {
  try {
    saveAllLoading.value = true

    // 模拟保存所有设置
    await new Promise(resolve => setTimeout(resolve, 2000))

    ElMessage.success('所有设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  } finally {
    saveAllLoading.value = false
  }
}

const handleResetAll = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置所有设置为默认值吗？此操作不可撤销！',
      '重置确认',
      {
        confirmButtonText: '确定重置',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    ElMessage.success('设置已重置为默认值')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置设置失败:', error)
    }
  }
}

const handleTestConnection = async () => {
  try {
    testLoading.value = true

    // 模拟测试连接
    await new Promise(resolve => setTimeout(resolve, 1500))

    ElMessage.success('连接测试成功')
  } catch (error) {
    console.error('连接测试失败:', error)
    ElMessage.error('连接测试失败')
  } finally {
    testLoading.value = false
  }
}

const handleExportConfig = () => {
  // 模拟导出配置
  const config = {
    basic: { siteName: '企业管理系统', version: '1.0.0' },
    security: { passwordPolicy: 'strong' },
    email: { smtp: 'smtp.example.com' }
  }

  const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'system-config.json'
  a.click()
  URL.revokeObjectURL(url)

  ElMessage.success('配置文件导出成功')
}

const handleImportConfig = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const config = JSON.parse(e.target.result)
          console.log('导入的配置:', config)
          ElMessage.success('配置文件导入成功')
        } catch (error) {
          ElMessage.error('配置文件格式错误')
        }
      }
      reader.readAsText(file)
    }
  }
  input.click()
}

const handleViewLogs = () => {
  router.push('/admin/settings/logs')
}

// 生命周期
onMounted(() => {
  // 如果当前路径是 /admin/settings，重定向到基础配置
  if (route.path === '/admin/settings') {
    router.replace('/admin/settings/basic')
  }
})
</script>

<style scoped>
.settings-page {
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

.header-actions {
  display: flex;
  gap: 12px;
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

/* 左侧导航 */
.settings-nav-card, .settings-status-card, .quick-operations-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.nav-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-icon {
  color: #409eff;
  font-size: 16px;
}

.nav-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.settings-nav {
  border: none;
}

.settings-nav .el-menu-item {
  border-radius: 8px;
  margin: 4px 0;
  transition: all 0.3s;
}

.settings-nav .el-menu-item:hover {
  background: #f0f9ff;
  color: #409eff;
}

.settings-nav .el-menu-item.is-active {
  background: linear-gradient(135deg, #409eff 0%, #36cfc9 100%);
  color: white;
}

/* 设置状态 */
.status-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.status-label {
  font-size: 13px;
  color: #606266;
}

/* 快速操作 */
.quick-operations {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-operations .el-button {
  justify-content: flex-start;
  text-align: left;
}

/* 右侧内容区域 */
.settings-content {
  min-height: 600px;
}

/* 过渡动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .settings-page .el-col:first-child {
    margin-bottom: 20px;
  }
}

@media (max-width: 768px) {
  .settings-page {
    padding: 12px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .page-title {
    font-size: 24px;
  }
}
</style>
