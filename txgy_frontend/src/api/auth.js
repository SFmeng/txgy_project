/**
 * 认证相关API接口
 */
import request from '@/utils/request'

export const authAPI = {
  /**
   * 用户登录
   */
  login(data) {
    return request({
      url: '/auth/login/',
      method: 'post',
      data
    })
  },

  /**
   * 用户注册
   */
  register(data) {
    return request({
      url: '/auth/register/',
      method: 'post',
      data
    })
  },

  /**
   * 用户登出
   */
  logout() {
    return request({
      url: '/auth/logout/',
      method: 'post'
    })
  },

  /**
   * 获取用户信息
   */
  getProfile() {
    return request({
      url: '/auth/profile/',
      method: 'get'
    })
  },

  /**
   * 更新用户信息
   */
  updateProfile(data) {
    return request({
      url: '/auth/profile/update/',
      method: 'put',
      data
    })
  },

  /**
   * 发送短信验证码
   */
  sendSmsCode(data) {
    return request({
      url: '/auth/sms/send/',
      method: 'post',
      data
    })
  },

  /**
   * 验证短信验证码
   */
  verifySmsCode(data) {
    return request({
      url: '/auth/sms/verify/',
      method: 'post',
      data
    })
  },

  /**
   * 修改密码
   */
  changePassword(data) {
    return request({
      url: '/auth/password/change/',
      method: 'post',
      data
    })
  },

  /**
   * 重置密码
   */
  resetPassword(data) {
    return request({
      url: '/auth/password/reset/',
      method: 'post',
      data
    })
  },

  /**
   * 企业认证
   */
  enterpriseVerify(data) {
    return request({
      url: '/auth/enterprise/verify/',
      method: 'post',
      data
    })
  },

  /**
   * 获取用户列表
   */
  getUserList(params = {}) {
    return request({
      url: '/auth/users/',
      method: 'get',
      params
    })
  },

  /**
   * 创建用户
   */
  createUser(data) {
    return request({
      url: '/auth/users/',
      method: 'post',
      data
    })
  },

  /**
   * 更新用户
   */
  updateUser(userId, data) {
    return request({
      url: `/auth/users/${userId}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除用户
   */
  deleteUser(userId) {
    return request({
      url: `/auth/users/${userId}/`,
      method: 'delete'
    })
  },

  /**
   * 获取Dashboard统计数据
   */
  getDashboardStats() {
    return request({
      url: '/auth/dashboard/stats/',
      method: 'get'
    })
  },

  /**
   * 获取用户权限和菜单
   */
  getUserPermissions() {
    return request({
      url: '/auth/permissions/',
      method: 'get'
    })
  },

  /**
   * 重置用户密码
   */
  resetUserPassword(userId) {
    return request({
      url: `/auth/users/${userId}/reset-password/`,
      method: 'post'
    })
  },

  /**
   * 分配用户角色
   */
  assignUserRoles(userId, roleIds) {
    return request({
      url: `/auth/users/${userId}/roles/`,
      method: 'post',
      data: { role_ids: roleIds }
    })
  },

  /**
   * 批量更新用户
   */
  batchUpdateUsers(userIds, data) {
    return request({
      url: '/auth/users/batch-update/',
      method: 'post',
      data: { user_ids: userIds, ...data }
    })
  },

  /**
   * 批量删除用户
   */
  batchDeleteUsers(userIds) {
    return request({
      url: '/auth/users/batch-delete/',
      method: 'post',
      data: { user_ids: userIds }
    })
  }
}
