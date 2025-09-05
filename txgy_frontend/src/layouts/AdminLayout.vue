<template>
  <div class="admin-layout">
    <el-container class="layout-container">
      <!-- 侧边栏 -->
      <el-aside :width="sidebarCollapsed ? '64px' : '240px'" class="sidebar">
        <div class="sidebar-header" @click="goToAdminHome">
          <div class="logo-section" v-if="!sidebarCollapsed">
            <div class="logo-icon">
              <el-icon :size="32" color="#ffffff">
                <Platform />
              </el-icon>
            </div>
            <span class="title">管理后台</span>
          </div>
          <div class="logo-collapsed" v-else>
            <el-icon :size="24" color="#ffffff">
              <Platform />
            </el-icon>
          </div>
        </div>
        
        <el-scrollbar class="sidebar-scrollbar">
          <!-- 菜单状态信息 -->
          <div class="menu-status-info">
            <div class="status-item">
              <el-icon><Menu /></el-icon>
              <span>菜单总数: {{ menuList.length }}</span>
            </div>
            <div class="status-item">
              <el-icon><Refresh /></el-icon>
              <span>状态: {{ menuStore.loading ? '加载中' : '已就绪' }}</span>
            </div>
          </div>

          <el-menu
            :default-active="activeMenu"
            :collapse="sidebarCollapsed"
            :unique-opened="true"
            background-color="transparent"
            text-color="rgba(255, 255, 255, 0.8)"
            active-text-color="#60a5fa"
            router
          >
            <!-- 完全由菜单管理系统控制的动态菜单 -->
            <template v-for="menu in menuList" :key="'menu-' + menu.menu_id">
              <!-- 有子菜单的情况 -->
              <el-sub-menu
                v-if="menu.children && menu.children.length > 0"
                :index="'sub-' + menu.menu_id"
                v-show="menu.status === 'active' && menu.is_show !== false"
              >
                <template #title>
                  <el-icon v-if="menu.icon">
                    <component :is="menu.icon" />
                  </el-icon>
                  <span>{{ menu.menu_name }}</span>
                </template>
                <el-menu-item
                  v-for="child in menu.children"
                  :key="'child-' + child.menu_id"
                  :index="child.path"
                  v-show="child.status === 'active' && child.is_show !== false"
                >
                  <el-icon v-if="child.icon">
                    <component :is="child.icon" />
                  </el-icon>
                  <span>{{ child.menu_name }}</span>
                </el-menu-item>
              </el-sub-menu>

              <!-- 单独菜单项的情况 -->
              <el-menu-item
                v-else-if="menu.path && menu.status === 'active' && menu.is_show !== false"
                :index="menu.path"
              >
                <el-icon v-if="menu.icon">
                  <component :is="menu.icon" />
                </el-icon>
                <span>{{ menu.menu_name }}</span>
              </el-menu-item>
            </template>

            <!-- 如果没有菜单数据，显示提示 -->
            <div v-if="!menuList || menuList.length === 0" class="no-menu-tip">
              <el-empty description="暂无菜单数据" :image-size="60">
                <el-button type="primary" size="small" @click="refreshMenus">
                  <el-icon><Refresh /></el-icon>
                  刷新菜单
                </el-button>
              </el-empty>
            </div>
          </el-menu>
        </el-scrollbar>
      </el-aside>

      <!-- 主内容区 -->
      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <el-button
              type="text"
              @click="toggleSidebar"
              class="sidebar-toggle"
            >
              <el-icon :size="20">
                <Fold v-if="!sidebarCollapsed" />
                <Expand v-else />
              </el-icon>
            </el-button>
            
            <el-breadcrumb separator="/" class="breadcrumb">
              <el-breadcrumb-item
                v-for="item in breadcrumbList"
                :key="item.path"
                :to="item.path"
              >
                {{ item.name }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>

          <div class="header-right">
            <!-- 主题切换 -->
            <el-dropdown @command="handleThemeChange" class="theme-dropdown">
              <el-button type="text" class="header-button">
                <el-icon :size="18">
                  <Sunny v-if="currentTheme === 'light'" />
                  <Moon v-else />
                </el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="light">
                    <el-icon><Sunny /></el-icon>
                    <span>浅色主题</span>
                  </el-dropdown-item>
                  <el-dropdown-item command="dark">
                    <el-icon><Moon /></el-icon>
                    <span>深色主题</span>
                  </el-dropdown-item>
                  <el-dropdown-item command="auto">
                    <el-icon><Monitor /></el-icon>
                    <span>跟随系统</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>

            <!-- 全屏切换 -->
            <el-button type="text" @click="toggleFullscreen" class="header-button">
              <el-icon :size="18">
                <FullScreen v-if="!isFullscreen" />
                <Aim v-else />
              </el-icon>
            </el-button>

            <!-- 消息通知 -->
            <el-badge :value="notificationCount" :hidden="notificationCount === 0">
              <el-button type="text" class="header-button">
                <el-icon :size="18">
                  <Bell />
                </el-icon>
              </el-button>
            </el-badge>

            <!-- 用户菜单 -->
            <el-dropdown @command="handleUserCommand" class="user-dropdown">
              <div class="user-info">
                <el-avatar :size="32" :src="userInfo?.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ userInfo?.real_name || userInfo?.username }}</span>
                <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    <span>个人中心</span>
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    <span>系统设置</span>
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    <span>退出登录</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 主要内容 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useMenuStore } from '@/stores/menu'
import {
  Platform,
  Fold,
  Expand,
  Sunny,
  Moon,
  Monitor,
  FullScreen,
  Aim,
  Bell,
  User,
  ArrowDown,
  Setting,
  SwitchButton,
  // 菜单图标
  DataBoard,
  UserFilled,
  Menu,
  OfficeBuilding,
  DocumentChecked,
  Shop
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const menuStore = useMenuStore()

// 响应式数据
const sidebarCollapsed = ref(false)
const isFullscreen = ref(false)
const notificationCount = ref(3)

// 计算属性
const userInfo = computed(() => authStore.userInfo)
const currentTheme = computed(() => themeStore.currentTheme)
const activeMenu = computed(() => route.path)
const menuList = computed(() => {
  const menus = menuStore.menuList
  console.log('🎯 AdminLayout: menuList计算属性被调用，菜单数量:', menus.length)
  console.log('🎯 AdminLayout: 菜单内容:', menus)
  console.log('🎯 AdminLayout: refreshTrigger:', menuStore.refreshTrigger)
  return menus
})

const breadcrumbList = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  return matched.map(item => ({
    name: item.meta.title,
    path: item.path
  }))
})

// 方法
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}

const handleThemeChange = (theme) => {
  themeStore.setTheme(theme)
}

const goToAdminHome = () => {
  router.push('/admin')
}

const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/admin/profile')
      break
    case 'settings':
      router.push('/admin/settings')
      break
    case 'logout':
      authStore.logout()
      router.push('/')
      break
  }
}

const loadUserMenus = async () => {
  console.log('🔄 AdminLayout: 开始加载用户菜单...')
  try {
    await menuStore.loadUserMenus()
    console.log('✅ AdminLayout: 菜单加载完成，当前菜单数量:', menuStore.menuList.length)
    console.log('📋 AdminLayout: 当前菜单列表:', menuStore.menuList)

    // 强制触发响应式更新
    await nextTick()
    console.log('🔄 AdminLayout: 强制更新完成')
  } catch (error) {
    console.error('❌ AdminLayout: 菜单加载失败:', error)
  }
}

// 刷新菜单
const refreshMenus = async () => {
  console.log('🔄 AdminLayout: 手动刷新菜单...')
  try {
    await menuStore.refreshMenus()
    console.log('✅ AdminLayout: 菜单刷新完成')
  } catch (error) {
    console.error('❌ AdminLayout: 菜单刷新失败:', error)
  }
}

// 监听全屏状态变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
}

onMounted(() => {
  loadUserMenus()
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

// 监听菜单刷新触发器
watch(() => menuStore.refreshTrigger, () => {
  // 当菜单刷新触发器变化时，菜单已经在store中更新了
  console.log('菜单已刷新')
})

// 监听主题变化
watch(currentTheme, (newTheme) => {
  document.documentElement.setAttribute('data-theme', newTheme)
}, { immediate: true })
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  overflow: hidden;
}

.layout-container {
  height: 100%;
}

.sidebar {
  background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #3730a3 100%);
  transition: width 0.3s ease;
  overflow: hidden;
  position: relative;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="sidebar-grid" width="30" height="30" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="30" height="30" fill="none"/><circle cx="15" cy="15" r="0.8" fill="rgba(59,130,246,0.2)"/><line x1="0" y1="15" x2="30" y2="15" stroke="rgba(59,130,246,0.1)" stroke-width="0.3"/><line x1="15" y1="0" x2="15" y2="30" stroke="rgba(59,130,246,0.1)" stroke-width="0.3"/></pattern></defs><rect width="100" height="100" fill="url(%23sidebar-grid)"/></svg>');
  opacity: 0.3;
  z-index: 1;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 58, 138, 0.9);
  border-bottom: 1px solid rgba(59, 130, 246, 0.3);
  cursor: pointer;
  transition: background-color 0.3s;
  position: relative;
  z-index: 2;
}

.sidebar-header:hover {
  background: rgba(30, 64, 175, 0.9);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  display: flex;
  align-items: center;
}

.title {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.logo-collapsed {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-scrollbar {
  height: calc(100vh - 60px);
  position: relative;
  z-index: 2;
}

/* 菜单状态信息 */
.menu-status-info {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 8px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  margin-bottom: 4px;
}

.status-item:last-child {
  margin-bottom: 0;
}

.status-item .el-icon {
  font-size: 14px;
}

/* 无菜单提示 */
.no-menu-tip {
  padding: 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.no-menu-tip .el-empty {
  --el-empty-description-color: rgba(255, 255, 255, 0.6);
}

.no-menu-tip .el-button {
  margin-top: 12px;
}

.main-container {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.header {
  background: linear-gradient(90deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
  position: relative;
}

.header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%);
  opacity: 0.6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.sidebar-toggle {
  color: #5a6169;
  font-size: 18px;
}

.breadcrumb {
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-button {
  color: #5a6169;
  padding: 8px;
}

.header-button:hover {
  background-color: #f5f7fa;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #303133;
}

.dropdown-icon {
  font-size: 12px;
  color: #909399;
}

.main-content {
  padding: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  overflow-y: auto;
  position: relative;
}

.main-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="main-grid" width="60" height="60" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="60" height="60" fill="none"/><circle cx="30" cy="30" r="1" fill="rgba(59,130,246,0.08)"/><line x1="0" y1="30" x2="60" y2="30" stroke="rgba(59,130,246,0.05)" stroke-width="0.5"/><line x1="30" y1="0" x2="30" y2="60" stroke="rgba(59,130,246,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23main-grid)"/></svg>');
  z-index: 0;
  pointer-events: none;
}

.main-content > * {
  position: relative;
  z-index: 1;
}

/* 深色主题样式 */
[data-theme="dark"] .header {
  background-color: #1f2937;
  border-bottom-color: #374151;
}

[data-theme="dark"] .main-content {
  background-color: #111827;
}

[data-theme="dark"] .user-info:hover {
  background-color: #374151;
}

[data-theme="dark"] .username {
  color: #f9fafb;
}

[data-theme="dark"] .header-button {
  color: #d1d5db;
}

[data-theme="dark"] .header-button:hover {
  background-color: #374151;
}
</style>
