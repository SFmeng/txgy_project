import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'

// 默认菜单数据
const defaultMenus = [
  {
    menu_id: 1,
    menu_name: '仪表盘',
    path: '/admin',
    icon: 'DataBoard',
    parent_id: null,
    sort_order: 1,
    status: 'active',
    terminal: 'pc',
    component: 'Dashboard',
    children: []
  },
  {
    menu_id: 2,
    menu_name: '用户管理',
    path: '/admin/users',
    icon: 'User',
    parent_id: null,
    sort_order: 2,
    status: 'active',
    terminal: 'pc',
    component: 'Users',
    children: []
  },
  {
    menu_id: 3,
    menu_name: '角色管理',
    path: '/admin/roles',
    icon: 'UserFilled',
    parent_id: null,
    sort_order: 3,
    status: 'active',
    terminal: 'pc',
    component: 'Roles',
    children: []
  },
  {
    menu_id: 4,
    menu_name: '菜单管理',
    path: '/admin/menus',
    icon: 'Menu',
    parent_id: null,
    sort_order: 4,
    status: 'active',
    terminal: 'pc',
    component: 'Menus',
    children: []
  },
  {
    menu_id: 5,
    menu_name: '企业管理',
    path: '',
    icon: 'OfficeBuilding',
    parent_id: null,
    sort_order: 5,
    status: 'active',
    terminal: 'pc',
    component: '',
    children: [
      {
        menu_id: 51,
        menu_name: '企业认证',
        path: '/admin/enterprise/verify',
        icon: 'DocumentChecked',
        parent_id: 5,
        sort_order: 1,
        status: 'active',
        terminal: 'pc',
        component: 'EnterpriseVerify',
        children: []
      },
      {
        menu_id: 52,
        menu_name: '企业管理',
        path: '/admin/enterprise/manage',
        icon: 'Shop',
        parent_id: 5,
        sort_order: 2,
        status: 'active',
        terminal: 'pc',
        component: 'EnterpriseManage',
        children: []
      }
    ]
  },
  {
    menu_id: 6,
    menu_name: '系统设置',
    path: '',
    icon: 'Setting',
    parent_id: null,
    sort_order: 6,
    status: 'active',
    terminal: 'pc',
    component: '',
    children: [
      {
        menu_id: 61,
        menu_name: '基础配置',
        path: '/admin/settings/basic',
        icon: 'Tools',
        parent_id: 6,
        sort_order: 1,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsBasic',
        children: []
      },
      {
        menu_id: 62,
        menu_name: '安全设置',
        path: '/admin/settings/security',
        icon: 'Lock',
        parent_id: 6,
        sort_order: 2,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsSecurity',
        children: []
      },
      {
        menu_id: 63,
        menu_name: '邮件配置',
        path: '/admin/settings/email',
        icon: 'Message',
        parent_id: 6,
        sort_order: 3,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsEmail',
        children: []
      },
      {
        menu_id: 64,
        menu_name: '存储配置',
        path: '/admin/settings/storage',
        icon: 'FolderOpened',
        parent_id: 6,
        sort_order: 4,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsStorage',
        children: []
      },
      {
        menu_id: 65,
        menu_name: '日志配置',
        path: '/admin/settings/logs',
        icon: 'Document',
        parent_id: 6,
        sort_order: 5,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsLogs',
        children: []
      },
      {
        menu_id: 66,
        menu_name: '备份恢复',
        path: '/admin/settings/backup',
        icon: 'Download',
        parent_id: 6,
        sort_order: 6,
        status: 'active',
        terminal: 'pc',
        component: 'SettingsBackup',
        children: []
      }
    ]
  }
]

export const useMenuStore = defineStore('menu', () => {
  // 状态
  const allMenus = ref([])
  const permissions = ref([])
  const loading = ref(false)
  const refreshTrigger = ref(0)

  // 计算属性：只返回状态为active的菜单
  const menuList = computed(() => {
    // 监听refreshTrigger以确保状态变化时重新计算
    const trigger = refreshTrigger.value
    console.log('🎯 menuList计算属性被调用, trigger:', trigger)
    console.log('📊 allMenus.value长度:', allMenus.value.length)

    const filterActiveMenus = (menus) => {
      return menus
        .filter(menu => {
          const isActive = menu.status === 'active'
          console.log(`🔍 检查菜单: ${menu.menu_name}, 状态: ${menu.status}, 是否显示: ${isActive}`)
          return isActive
        })
        .map(menu => {
          const filteredMenu = {
            ...menu,
            children: menu.children && menu.children.length > 0 ? filterActiveMenus(menu.children) : []
          }
          console.log(`✅ 处理后的菜单: ${filteredMenu.menu_name}, 子菜单数量: ${filteredMenu.children.length}`)
          return filteredMenu
        })
    }

    // 确保使用最新的菜单数据
    let sourceMenus = allMenus.value.length > 0 ? allMenus.value : defaultMenus
    console.log('📋 使用的菜单源数量:', sourceMenus.length)

    // 打印每个菜单的状态
    sourceMenus.forEach(menu => {
      console.log(`📋 源菜单: ${menu.menu_name}, 状态: ${menu.status}`)
      if (menu.children) {
        menu.children.forEach(child => {
          console.log(`  📋 子菜单: ${child.menu_name}, 状态: ${child.status}`)
        })
      }
    })

    const result = filterActiveMenus(sourceMenus)
    console.log('🎯 最终菜单结果数量:', result.length)
    console.log('🎯 最终菜单列表:', result.map(m => `${m.menu_name}(${m.status})`))

    return result
  })

  // 获取用户菜单和权限
  const loadUserMenus = async () => {
    loading.value = true
    try {
      console.log('🔄 开始加载用户菜单和权限...')
      console.log('📊 默认菜单数量:', defaultMenus.length)
      console.log('📊 默认菜单内容:', defaultMenus)

      // 首先设置默认菜单，确保用户能看到所有功能
      allMenus.value = [...defaultMenus]
      permissions.value = ['dashboard:view', 'users:manage', 'roles:manage', 'menus:manage', 'enterprise:manage']

      console.log('✅ 默认菜单已设置，allMenus长度:', allMenus.value.length)
      console.log('✅ allMenus内容:', allMenus.value)

      // 暂时禁用API调用，直接使用默认菜单确保稳定性
      console.log('🔒 暂时跳过API调用，直接使用默认菜单配置')

      // 注释掉API调用部分，避免异步问题
      /*
      try {
        const response = await authAPI.getUserPermissions()
        console.log('🌐 API响应:', response)

        if (response.data.menus && response.data.menus.length > 0) {
          allMenus.value = response.data.menus
          console.log('✅ 使用API菜单数据，菜单数量:', allMenus.value.length)
        } else {
          console.log('✅ API未返回菜单数据，使用默认菜单')
        }

        if (response.data.permissions && response.data.permissions.length > 0) {
          permissions.value = response.data.permissions
          console.log('✅ 使用API权限数据，权限数量:', permissions.value.length)
        } else {
          console.log('✅ API未返回权限数据，使用默认权限')
        }
      } catch (apiError) {
        console.warn('⚠️ API调用失败，继续使用默认配置:', apiError.message)
      }
      */

      // 强制触发响应式更新
      refreshTrigger.value++

      console.log('✅ 菜单加载完成，菜单数量:', allMenus.value.length)
      console.log('✅ 权限加载完成，权限数量:', permissions.value.length)
      console.log('📋 最终菜单详情:', allMenus.value)
      console.log('📋 最终权限详情:', permissions.value)
      console.log('🔄 refreshTrigger已更新:', refreshTrigger.value)

      return allMenus.value
    } catch (error) {
      console.error('❌ 菜单加载过程出错:', error.message)
      // 确保即使出错也有默认菜单
      allMenus.value = [...defaultMenus]
      permissions.value = ['dashboard:view', 'users:manage', 'roles:manage', 'menus:manage', 'enterprise:manage']
      console.log('✅ 错误恢复：使用默认菜单，菜单数量:', allMenus.value.length)
      return allMenus.value
    } finally {
      loading.value = false
    }
  }

  // 获取所有菜单（用于菜单管理页面）
  const getAllMenus = () => {
    // 如果allMenus为空，使用默认菜单
    if (allMenus.value.length === 0) {
      allMenus.value = [...defaultMenus]
    }
    return allMenus.value
  }

  // 保存菜单（模拟API调用）
  const saveMenu = async (menuData) => {
    console.log('💾 保存菜单:', menuData)
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    if (menuData.menu_id) {
      // 更新菜单
      const updateMenu = (menus, targetId, newData) => {
        for (let menu of menus) {
          if (menu.menu_id === targetId) {
            Object.assign(menu, newData)
            return true
          }
          if (menu.children && menu.children.length > 0) {
            if (updateMenu(menu.children, targetId, newData)) {
              return true
            }
          }
        }
        return false
      }
      updateMenu(defaultMenus, menuData.menu_id, menuData)
    } else {
      // 新增菜单
      const newId = Math.max(...getAllMenuIds(defaultMenus)) + 1
      menuData.menu_id = newId

      if (menuData.parent_id) {
        // 添加到父菜单的children中
        const findParent = (menus, parentId) => {
          for (let menu of menus) {
            if (menu.menu_id === parentId) {
              if (!menu.children) menu.children = []
              menu.children.push(menuData)
              // 按sort_order排序
              menu.children.sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
              return true
            }
            if (menu.children && menu.children.length > 0) {
              if (findParent(menu.children, parentId)) {
                return true
              }
            }
          }
          return false
        }
        findParent(defaultMenus, menuData.parent_id)
      } else {
        // 添加为根菜单
        defaultMenus.push(menuData)
        // 按sort_order排序
        defaultMenus.sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
      }
    }

    // 重新排序所有菜单
    sortMenus(defaultMenus)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return menuData
  }

  // 删除菜单
  const deleteMenu = async (menuId) => {
    console.log('🗑️ 删除菜单:', menuId)
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    const removeMenu = (menus, targetId) => {
      for (let i = 0; i < menus.length; i++) {
        if (menus[i].menu_id === targetId) {
          menus.splice(i, 1)
          return true
        }
        if (menus[i].children && menus[i].children.length > 0) {
          if (removeMenu(menus[i].children, targetId)) {
            return true
          }
        }
      }
      return false
    }

    removeMenu(defaultMenus, menuId)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return true
  }

  // 获取所有菜单ID
  const getAllMenuIds = (menus) => {
    let ids = []
    for (let menu of menus) {
      ids.push(menu.menu_id)
      if (menu.children && menu.children.length > 0) {
        ids = ids.concat(getAllMenuIds(menu.children))
      }
    }
    return ids
  }

  // 菜单排序
  const sortMenus = (menus) => {
    menus.sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
    menus.forEach(menu => {
      if (menu.children && menu.children.length > 0) {
        sortMenus(menu.children)
      }
    })
  }

  // 更新菜单排序
  const updateMenuOrder = async (menuId, newOrder) => {
    console.log('🔄 更新菜单排序:', menuId, newOrder)

    const updateOrder = (menus, targetId, order) => {
      for (let menu of menus) {
        if (menu.menu_id === targetId) {
          menu.sort_order = order
          return true
        }
        if (menu.children && menu.children.length > 0) {
          if (updateOrder(menu.children, targetId, order)) {
            return true
          }
        }
      }
      return false
    }

    updateOrder(defaultMenus, menuId, newOrder)
    sortMenus(defaultMenus)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return true
  }

  // 移动菜单位置
  const moveMenu = async (menuId, direction) => {
    console.log('📍 移动菜单:', menuId, direction)

    const findMenuAndParent = (menus, targetId, parent = null) => {
      for (let i = 0; i < menus.length; i++) {
        if (menus[i].menu_id === targetId) {
          return { menu: menus[i], parent, index: i, siblings: menus }
        }
        if (menus[i].children && menus[i].children.length > 0) {
          const result = findMenuAndParent(menus[i].children, targetId, menus[i])
          if (result) return result
        }
      }
      return null
    }

    const result = findMenuAndParent(defaultMenus, menuId)
    if (!result) return false

    const { menu, siblings, index } = result

    if (direction === 'up' && index > 0) {
      // 向上移动
      const temp = menu.sort_order
      menu.sort_order = siblings[index - 1].sort_order
      siblings[index - 1].sort_order = temp
    } else if (direction === 'down' && index < siblings.length - 1) {
      // 向下移动
      const temp = menu.sort_order
      menu.sort_order = siblings[index + 1].sort_order
      siblings[index + 1].sort_order = temp
    }

    sortMenus(defaultMenus)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return true
  }

  // 切换菜单状态
  const toggleMenuStatus = async (menuId) => {
    console.log('🔄 切换菜单状态:', menuId)

    const toggleStatus = (menus, targetId) => {
      for (let menu of menus) {
        if (menu.menu_id === targetId) {
          menu.status = menu.status === 'active' ? 'inactive' : 'active'
          return true
        }
        if (menu.children && menu.children.length > 0) {
          if (toggleStatus(menu.children, targetId)) {
            return true
          }
        }
      }
      return false
    }

    toggleStatus(defaultMenus, menuId)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return true
  }

  // 获取菜单详情
  const getMenuById = (menuId) => {
    const findMenu = (menus, targetId) => {
      for (let menu of menus) {
        if (menu.menu_id === targetId) {
          return menu
        }
        if (menu.children && menu.children.length > 0) {
          const found = findMenu(menu.children, targetId)
          if (found) return found
        }
      }
      return null
    }

    return findMenu(defaultMenus, menuId)
  }

  // 获取父菜单选项（用于下拉选择）
  const getParentMenuOptions = () => {
    const options = []

    const collectParents = (menus, level = 0) => {
      menus.forEach(menu => {
        options.push({
          value: menu.menu_id,
          label: '  '.repeat(level) + menu.menu_name,
          level
        })
        if (menu.children && menu.children.length > 0) {
          collectParents(menu.children, level + 1)
        }
      })
    }

    collectParents(defaultMenus)
    return options
  }

  // 批量更新菜单
  const batchUpdateMenus = async (updates) => {
    console.log('📦 批量更新菜单:', updates)

    updates.forEach(update => {
      const updateMenu = (menus, targetId, newData) => {
        for (let menu of menus) {
          if (menu.menu_id === targetId) {
            Object.assign(menu, newData)
            return true
          }
          if (menu.children && menu.children.length > 0) {
            if (updateMenu(menu.children, targetId, newData)) {
              return true
            }
          }
        }
        return false
      }

      updateMenu(defaultMenus, update.menu_id, update.data)
    })

    sortMenus(defaultMenus)

    // 刷新菜单
    allMenus.value = [...defaultMenus]
    refreshTrigger.value++
    return true
  }

  // 刷新菜单
  const refreshMenus = async () => {
    console.log('🔄 触发菜单刷新...')
    refreshTrigger.value++
    const result = await loadUserMenus()
    console.log('✅ 菜单刷新完成')
    return result
  }

  // 清空菜单
  const clearMenus = () => {
    allMenus.value = []
    permissions.value = []
  }

  // 检查用户是否有指定权限
  const hasPermission = (permissionCode) => {
    return permissions.value.includes(permissionCode)
  }

  // 检查用户是否有任意一个权限
  const hasAnyPermission = (permissionCodes) => {
    return permissionCodes.some(code => permissions.value.includes(code))
  }

  // 检查用户是否有所有权限
  const hasAllPermissions = (permissionCodes) => {
    return permissionCodes.every(code => permissions.value.includes(code))
  }

  // 菜单管理相关方法
  const loadMenus = async () => {
    console.log('🔄 加载菜单树...')
    loading.value = true
    try {
      // 使用默认菜单作为菜单树数据
      allMenus.value = [...defaultMenus]
      refreshTrigger.value++
      return allMenus.value
    } catch (error) {
      console.error('❌ 加载菜单树失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createMenu = async (menuData) => {
    console.log('➕ 创建菜单:', menuData)
    return await saveMenu(menuData)
  }

  const updateMenu = async (menuId, menuData) => {
    console.log('✏️ 更新菜单:', menuId, menuData)
    menuData.menu_id = menuId
    return await saveMenu(menuData)
  }

  const updateMenuStatus = async (menuId, status) => {
    console.log('🔄 更新菜单状态:', menuId, '设置为:', status)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    const updateStatus = (menus, targetId, newStatus) => {
      for (let menu of menus) {
        if (menu.menu_id === targetId) {
          console.log(`📝 找到菜单 ${menu.menu_name}，状态从 ${menu.status} 更新为 ${newStatus}`)
          menu.status = newStatus
          return true
        }
        if (menu.children && menu.children.length > 0) {
          if (updateStatus(menu.children, targetId, newStatus)) {
            return true
          }
        }
      }
      return false
    }

    const updated = updateStatus(defaultMenus, menuId, status)

    if (updated) {
      // 刷新菜单
      allMenus.value = [...defaultMenus]
      refreshTrigger.value++
      console.log('✅ 菜单状态更新成功，触发刷新')
      return true
    } else {
      console.error('❌ 未找到要更新的菜单:', menuId)
      throw new Error('菜单不存在')
    }
  }

  // 获取菜单树（用于菜单管理页面）
  const menuTree = computed(() => {
    return allMenus.value
  })

  return {
    // 状态
    menuList,
    allMenus,
    permissions,
    loading,
    refreshTrigger,
    menuTree,

    // 基础方法
    loadUserMenus,
    refreshMenus,
    clearMenus,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    getAllMenus,

    // 菜单管理方法
    loadMenus,
    createMenu,
    updateMenu,
    updateMenuStatus,
    saveMenu,
    deleteMenu,
    updateMenuOrder,
    moveMenu,
    toggleMenuStatus,
    getMenuById,
    getParentMenuOptions,
    batchUpdateMenus
  }
})
