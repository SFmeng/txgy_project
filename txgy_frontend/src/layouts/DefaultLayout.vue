<template>
  <div class="default-layout">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <!-- Logo和标题 -->
        <div class="logo-section">
          <router-link to="/" class="logo-link">
            <div class="logo-icon">
              <el-icon :size="32" color="#3b82f6">
                <Platform />
              </el-icon>
            </div>
            <span class="title">防腐保温智慧平台</span>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          class="nav-menu"
          router
        >
          <el-menu-item index="/products">产品中心</el-menu-item>
          <el-menu-item index="/search">搜索匹配</el-menu-item>
          <el-menu-item index="/resources">资源中心</el-menu-item>
          <el-menu-item index="/bidding">招投标</el-menu-item>
        </el-menu>

        <!-- 用户操作区 -->
        <div class="user-section">
          <template v-if="authStore.isLoggedIn">
            <!-- 消息通知 -->
            <el-badge :value="unreadCount" class="notification-badge">
              <el-button :icon="Bell" circle />
            </el-badge>

            <!-- 用户菜单 -->
            <el-dropdown @command="handleUserCommand">
              <div class="user-info">
                <el-avatar :src="authStore.userInfo?.avatar" :size="32">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ authStore.userInfo?.real_name || authStore.userInfo?.username }}</span>
                <el-icon class="arrow-down"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="dashboard">
                    <el-icon><House /></el-icon>
                    工作台
                  </el-dropdown-item>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          
          <template v-else>
            <el-button @click="$router.push('/auth/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/auth/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <router-view />
    </el-main>

    <!-- 底部 -->
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-info">
          <p>&copy; 2024 防腐保温智慧平台. All rights reserved.</p>
          <div class="footer-links">
            <a href="/about">关于我们</a>
            <a href="/contact">联系我们</a>
            <a href="/privacy">隐私政策</a>
            <a href="/terms">服务条款</a>
          </div>
        </div>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Bell,
  User,
  ArrowDown,
  House,
  Setting,
  SwitchButton,
  Platform
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const unreadCount = ref(0)

const activeMenu = computed(() => {
  return route.path
})

// 处理用户菜单命令
const handleUserCommand = async (command) => {
  switch (command) {
    case 'dashboard':
      if (authStore.isEnterprise) {
        router.push('/dashboard/enterprise')
      } else {
        router.push('/dashboard/individual')
      }
      break
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await authStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/')
      } catch (error) {
        // 用户取消操作
      }
      break
  }
}

onMounted(() => {
  // 获取未读消息数量
  // TODO: 实现获取未读消息数量的逻辑
})
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0;
  height: 60px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.logo-icon {
  display: flex;
  align-items: center;
  margin-right: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.nav-menu {
  flex: 1;
  margin: 0 40px;
  border-bottom: none;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-badge {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #606266;
}

.arrow-down {
  font-size: 12px;
  color: #909399;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: #f5f7fa;
  border-top: 1px solid #e4e7ed;
  padding: 20px 0;
  height: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-info {
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.footer-links {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.footer-links a {
  color: #909399;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #409eff;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }
  
  .nav-menu {
    display: none;
  }
  
  .title {
    font-size: 16px;
  }
  
  .main-content {
    padding: 10px;
  }
}
</style>
