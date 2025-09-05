import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/pages/auth/Login.vue'),
        meta: { title: '登录', requiresGuest: true }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/pages/auth/Register.vue'),
        meta: { title: '注册', requiresGuest: true }
      }
    ]
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'enterprise',
        name: 'EnterpriseDashboard',
        component: () => import('@/pages/dashboard/Enterprise.vue'),
        meta: { title: '企业工作台', requiresAuth: true, userType: 'enterprise' }
      },
      {
        path: 'individual',
        name: 'IndividualDashboard',
        component: () => import('@/pages/dashboard/Individual.vue'),
        meta: { title: '个人工作台', requiresAuth: true, userType: 'individual' }
      }
    ]
  },
  {
    path: '/products',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'ProductList',
        component: () => import('@/pages/products/ProductList.vue'),
        meta: { title: '产品列表' }
      },
      {
        path: ':id',
        name: 'ProductDetail',
        component: () => import('@/pages/products/ProductDetail.vue'),
        meta: { title: '产品详情' }
      }
    ]
  },
  {
    path: '/search',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'Search',
        component: () => import('@/pages/search/Search.vue'),
        meta: { title: '搜索' }
      }
    ]
  },
  {
    path: '/profile',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Profile',
        component: () => import('@/pages/profile/Profile.vue'),
        meta: { title: '个人资料', requiresAuth: true }
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/Dashboard.vue'),
        meta: { title: '管理后台', requiresAuth: true }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/Users.vue'),
        meta: { title: '用户管理', requiresAuth: true }
      },
      {
        path: 'enterprise',
        name: 'AdminEnterprise',
        component: () => import('@/pages/admin/Enterprise.vue'),
        meta: { title: '企业管理', requiresAuth: true },
        children: [
          {
            path: '',
            redirect: 'verify'
          },
          {
            path: 'verify',
            name: 'EnterpriseVerify',
            component: () => import('@/pages/admin/enterprise/Verify.vue'),
            meta: { title: '企业认证', requiresAuth: true }
          },
          {
            path: 'manage',
            name: 'EnterpriseManage',
            component: () => import('@/pages/admin/enterprise/Manage.vue'),
            meta: { title: '企业管理', requiresAuth: true }
          }
        ]
      },
      {
        path: 'user-stats',
        name: 'AdminUserStats',
        component: () => import('@/pages/admin/UserStats.vue'),
        meta: { title: '用户统计', requiresAuth: true }
      },
      {
        path: 'roles',
        name: 'AdminRoles',
        component: () => import('@/pages/admin/Roles.vue'),
        meta: { title: '角色管理', requiresAuth: true }
      },
      {
        path: 'permissions',
        name: 'AdminPermissions',
        component: () => import('@/pages/admin/Permissions.vue'),
        meta: { title: '权限管理', requiresAuth: true }
      },
      {
        path: 'menus',
        name: 'AdminMenus',
        component: () => import('@/pages/admin/Menus.vue'),
        meta: { title: '菜单管理', requiresAuth: true }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/pages/admin/Settings.vue'),
        meta: { title: '系统设置', requiresAuth: true },
        children: [
          {
            path: '',
            redirect: 'basic'
          },
          {
            path: 'basic',
            name: 'SettingsBasic',
            component: () => import('@/pages/admin/settings/Basic.vue'),
            meta: { title: '基础配置', requiresAuth: true }
          },
          {
            path: 'security',
            name: 'SettingsSecurity',
            component: () => import('@/pages/admin/settings/Security.vue'),
            meta: { title: '安全设置', requiresAuth: true }
          },
          {
            path: 'email',
            name: 'SettingsEmail',
            component: () => import('@/pages/admin/settings/Email.vue'),
            meta: { title: '邮件配置', requiresAuth: true }
          },
          {
            path: 'storage',
            name: 'SettingsStorage',
            component: () => import('@/pages/admin/settings/Storage.vue'),
            meta: { title: '存储配置', requiresAuth: true }
          },
          {
            path: 'logs',
            name: 'SettingsLogs',
            component: () => import('@/pages/admin/settings/Logs.vue'),
            meta: { title: '日志配置', requiresAuth: true }
          },
          {
            path: 'backup',
            name: 'SettingsBackup',
            component: () => import('@/pages/admin/settings/Backup.vue'),
            meta: { title: '备份恢复', requiresAuth: true }
          }
        ]
      },
      {
        path: 'profile',
        name: 'AdminProfile',
        component: () => import('@/pages/admin/Profile.vue'),
        meta: { title: '个人中心', requiresAuth: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 防腐保温智慧平台` : '防腐保温智慧平台'
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
    
    // 检查用户类型
    if (to.meta.userType && authStore.userInfo?.user_type !== to.meta.userType) {
      next({ name: 'Home' })
      return
    }
  }
  
  // 检查是否需要游客状态（如登录、注册页面）
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    next({ name: 'AdminDashboard' })
    return
  }
  
  next()
})

export default router
