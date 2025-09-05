/**
 * 组织架构API
 */
import request from '@/utils/request'

export const organizationAPI = {
  /**
   * 获取角色列表
   */
  getRoles(params = {}) {
    return request({
      url: '/organization/roles/',
      method: 'get',
      params
    })
  },

  /**
   * 创建角色
   */
  createRole(data) {
    return request({
      url: '/organization/roles/',
      method: 'post',
      data
    })
  },

  /**
   * 获取角色详情
   */
  getRoleDetail(roleId) {
    return request({
      url: `/organization/roles/${roleId}/`,
      method: 'get'
    })
  },

  /**
   * 更新角色
   */
  updateRole(roleId, data) {
    return request({
      url: `/organization/roles/${roleId}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除角色
   */
  deleteRole(roleId) {
    return request({
      url: `/organization/roles/${roleId}/`,
      method: 'delete'
    })
  },

  /**
   * 获取权限列表
   */
  getPermissions(params = {}) {
    // 如果需要按模块分组，使用新的管理API
    if (params.group_by_module) {
      return request({
        url: '/organization/permissions/manage/',
        method: 'get',
        params
      })
    }

    return request({
      url: '/organization/permissions/manage/',
      method: 'get',
      params
    })
  },

  /**
   * 获取菜单树
   */
  getMenuTree(params = {}) {
    return request({
      url: '/organization/menus/tree/',
      method: 'get',
      params
    })
  },

  /**
   * 获取用户权限和菜单
   */
  getUserPermissions() {
    return request({
      url: '/organization/user/permissions/',
      method: 'get'
    })
  },

  /**
   * 分配角色给用户
   */
  assignRoles(data) {
    return request({
      url: '/organization/assign/roles/',
      method: 'post',
      data
    })
  },

  /**
   * 分配权限给角色
   */
  assignPermissions(data) {
    return request({
      url: '/organization/assign/permissions/',
      method: 'post',
      data
    })
  },

  /**
   * 分配菜单给角色
   */
  assignMenus(data) {
    return request({
      url: '/organization/assign/menus/',
      method: 'post',
      data
    })
  },

  /**
   * 获取操作日志
   */
  getOperationLogs(params = {}) {
    return request({
      url: '/organization/logs/',
      method: 'get',
      params
    })
  },

  /**
   * 获取系统配置
   */
  getSystemConfigs(params = {}) {
    return request({
      url: '/organization/configs/',
      method: 'get',
      params
    })
  },

  /**
   * 创建系统配置
   */
  createSystemConfig(data) {
    return request({
      url: '/organization/configs/',
      method: 'post',
      data
    })
  },

  /**
   * 更新系统配置
   */
  updateSystemConfig(configId, data) {
    return request({
      url: `/organization/configs/${configId}/`,
      method: 'put',
      data
    })
  },

  /**
   * 创建菜单
   */
  createMenu(data) {
    return request({
      url: '/organization/menus/',
      method: 'post',
      data
    })
  },

  /**
   * 更新菜单
   */
  updateMenu(menuId, data) {
    return request({
      url: `/organization/menus/${menuId}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除菜单
   */
  deleteMenu(menuId) {
    return request({
      url: `/organization/menus/${menuId}/`,
      method: 'delete'
    })
  },

  /**
   * 创建权限
   */
  createPermission(data) {
    return request({
      url: '/organization/permissions/manage/',
      method: 'post',
      data
    })
  },

  /**
   * 更新权限
   */
  updatePermission(permissionId, data) {
    return request({
      url: `/organization/permissions/${permissionId}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除权限
   */
  deletePermission(permissionId) {
    return request({
      url: `/organization/permissions/${permissionId}/`,
      method: 'delete'
    })
  }
}
