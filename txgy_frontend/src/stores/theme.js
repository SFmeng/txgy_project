/**
 * 主题管理Store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const theme = ref(localStorage.getItem('theme') || 'light')
  const systemTheme = ref('light')
  
  // 计算属性
  const currentTheme = computed(() => {
    if (theme.value === 'auto') {
      return systemTheme.value
    }
    return theme.value
  })
  
  const isDark = computed(() => currentTheme.value === 'dark')
  
  // 主题配置
  const themeConfig = {
    light: {
      name: '浅色主题',
      primary: '#409EFF',
      success: '#67C23A',
      warning: '#E6A23C',
      danger: '#F56C6C',
      info: '#909399',
      background: '#ffffff',
      surface: '#f5f7fa',
      text: '#303133',
      textSecondary: '#606266',
      border: '#dcdfe6'
    },
    dark: {
      name: '深色主题',
      primary: '#409EFF',
      success: '#67C23A',
      warning: '#E6A23C',
      danger: '#F56C6C',
      info: '#909399',
      background: '#1f2937',
      surface: '#111827',
      text: '#f9fafb',
      textSecondary: '#d1d5db',
      border: '#374151'
    }
  }
  
  // 方法
  const setTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }
  
  const applyTheme = () => {
    const root = document.documentElement
    const config = themeConfig[currentTheme.value]
    
    // 设置CSS变量
    Object.entries(config).forEach(([key, value]) => {
      if (key !== 'name') {
        root.style.setProperty(`--theme-${key}`, value)
      }
    })
    
    // 设置data-theme属性
    root.setAttribute('data-theme', currentTheme.value)
    
    // 设置Element Plus主题
    if (currentTheme.value === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }
  
  const detectSystemTheme = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    systemTheme.value = mediaQuery.matches ? 'dark' : 'light'
    
    // 监听系统主题变化
    mediaQuery.addEventListener('change', (e) => {
      systemTheme.value = e.matches ? 'dark' : 'light'
      if (theme.value === 'auto') {
        applyTheme()
      }
    })
  }
  
  const toggleTheme = () => {
    const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }
  
  const getThemeConfig = (themeName = null) => {
    return themeConfig[themeName || currentTheme.value]
  }
  
  const initTheme = () => {
    detectSystemTheme()
    applyTheme()
  }
  
  // 预设主题
  const presetThemes = [
    {
      name: '默认蓝',
      key: 'default-blue',
      primary: '#409EFF',
      colors: {
        primary: '#409EFF',
        success: '#67C23A',
        warning: '#E6A23C',
        danger: '#F56C6C',
        info: '#909399'
      }
    },
    {
      name: '科技紫',
      key: 'tech-purple',
      primary: '#722ED1',
      colors: {
        primary: '#722ED1',
        success: '#52C41A',
        warning: '#FAAD14',
        danger: '#FF4D4F',
        info: '#8C8C8C'
      }
    },
    {
      name: '商务绿',
      key: 'business-green',
      primary: '#13C2C2',
      colors: {
        primary: '#13C2C2',
        success: '#52C41A',
        warning: '#FAAD14',
        danger: '#FF4D4F',
        info: '#8C8C8C'
      }
    },
    {
      name: '活力橙',
      key: 'vibrant-orange',
      primary: '#FA8C16',
      colors: {
        primary: '#FA8C16',
        success: '#52C41A',
        warning: '#FAAD14',
        danger: '#FF4D4F',
        info: '#8C8C8C'
      }
    }
  ]
  
  const applyPresetTheme = (presetKey) => {
    const preset = presetThemes.find(p => p.key === presetKey)
    if (!preset) return
    
    const root = document.documentElement
    Object.entries(preset.colors).forEach(([key, value]) => {
      root.style.setProperty(`--el-color-${key}`, value)
    })
    
    localStorage.setItem('preset-theme', presetKey)
  }
  
  const getCurrentPresetTheme = () => {
    return localStorage.getItem('preset-theme') || 'default-blue'
  }
  
  return {
    // 状态
    theme,
    systemTheme,
    
    // 计算属性
    currentTheme,
    isDark,
    
    // 方法
    setTheme,
    applyTheme,
    detectSystemTheme,
    toggleTheme,
    getThemeConfig,
    initTheme,
    
    // 预设主题
    presetThemes,
    applyPresetTheme,
    getCurrentPresetTheme
  }
})
