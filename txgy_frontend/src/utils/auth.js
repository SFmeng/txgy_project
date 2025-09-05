/**
 * 认证相关工具函数
 */

const TOKEN_KEY = 'txgy_token'

/**
 * 获取Token
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * 设置Token
 */
export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

/**
 * 移除Token
 */
export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

/**
 * 检查Token是否存在
 */
export function hasToken() {
  return !!getToken()
}

/**
 * 解析JWT Token
 */
export function parseToken(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Token解析失败:', error)
    return null
  }
}

/**
 * 检查Token是否过期
 */
export function isTokenExpired(token) {
  const payload = parseToken(token)
  if (!payload || !payload.exp) {
    return true
  }
  
  const currentTime = Math.floor(Date.now() / 1000)
  return payload.exp < currentTime
}
