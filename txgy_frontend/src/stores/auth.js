import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'
import { setToken, removeToken, getToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(getToken())
  const userInfo = ref(null)
  const permissions = ref([])

  // 初始化时从localStorage恢复用户信息
  const initUserInfo = () => {
    try {
      const storedUserInfo = localStorage.getItem('user_info')
      if (storedUserInfo) {
        const parsed = JSON.parse(storedUserInfo)
        userInfo.value = parsed
        permissions.value = parsed.permissions || []
        console.log('🔄 从localStorage恢复用户信息:', parsed)
      }
    } catch (error) {
      console.error('恢复用户信息失败:', error)
    }
  }

  // 立即初始化
  if (token.value) {
    initUserInfo()
  }

  const isLoggedIn = computed(() => !!token.value)
  const isEnterprise = computed(() => userInfo.value?.user_type === 'enterprise')
  const isIndividual = computed(() => userInfo.value?.user_type === 'individual')

  // 登录
  const login = async (loginData) => {
    try {
      const response = await authAPI.login(loginData)
      const { access_token, user_info } = response.data

      token.value = access_token
      userInfo.value = user_info
      permissions.value = user_info.permissions || []

      setToken(access_token)
      // 保存用户信息到localStorage
      localStorage.setItem('user_info', JSON.stringify(user_info))

      console.log('🔄 登录成功，用户信息已保存:', user_info)
      return response
    } catch (error) {
      throw error
    }
  }

  // 登出
  const logout = async () => {
    try {
      if (token.value) {
        await authAPI.logout()
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      token.value = null
      userInfo.value = null
      permissions.value = []
      removeToken()
      // 清除用户信息
      localStorage.removeItem('user_info')
      console.log('🔄 登出成功，用户信息已清除')
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await authAPI.getProfile()
      userInfo.value = response.data
      permissions.value = response.data.permissions || []
      return response
    } catch (error) {
      // 如果获取用户信息失败，清除登录状态
      logout()
      throw error
    }
  }

  // 检查认证状态
  const checkAuthStatus = async () => {
    if (token.value && !userInfo.value) {
      try {
        await fetchUserInfo()
      } catch (error) {
        console.error('检查认证状态失败:', error)
      }
    }
  }

  // 检查权限
  const hasPermission = (permission) => {
    return permissions.value.includes(permission)
  }

  // 更新用户信息
  const updateUserInfo = (newUserInfo) => {
    userInfo.value = { ...userInfo.value, ...newUserInfo }
  }

  return {
    token,
    userInfo,
    permissions,
    isLoggedIn,
    isEnterprise,
    isIndividual,
    login,
    logout,
    fetchUserInfo,
    checkAuthStatus,
    hasPermission,
    updateUserInfo
  }
})
