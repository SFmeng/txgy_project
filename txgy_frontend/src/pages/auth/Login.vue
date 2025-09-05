<template>
  <div class="login-container" role="main" aria-label="用户登录页面">
    <!-- 登录表单区域 -->
    <div class="form-section">
        <div class="form-container">
          <!-- Logo和标题 -->
          <div class="logo-section">
            <div class="logo-icon">
              <el-icon :size="40">
                <Platform />
              </el-icon>
            </div>
            <h1 class="platform-title">防腐保温行业平台</h1>
          </div>

          <div class="form-header">
            <h2 class="form-title">欢迎回来</h2>
            <p class="form-subtitle">登录您的账户以继续使用平台服务</p>
          </div>

          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            size="large"
          >
            <el-form-item prop="username">
              <div class="input-wrapper">
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名或手机号"
                  prefix-icon="User"
                  clearable
                  class="modern-input"
                  autocomplete="username"
                  @keyup.enter="handleLogin"
                />
              </div>
            </el-form-item>

            <el-form-item prop="password">
              <div class="input-wrapper">
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  show-password
                  clearable
                  class="modern-input"
                  autocomplete="current-password"
                  @keyup.enter="handleLogin"
                />
              </div>
            </el-form-item>

            <el-form-item>
              <div class="login-options">
                <el-checkbox v-model="loginForm.remember" class="remember-checkbox">
                  记住我
                </el-checkbox>
                <el-link type="primary" @click="showForgotPassword" class="forgot-link">
                  忘记密码？
                </el-link>
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                :disabled="loading"
                @click="handleLogin"
              >
                <span v-if="!loading">登录</span>
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <p class="register-prompt">
              还没有账号？
              <router-link to="/auth/register" class="register-link">
                立即注册
              </router-link>
            </p>
          </div>
        </div>
      </div>

    <!-- 忘记密码对话框 -->
    <el-dialog
      v-model="forgotPasswordVisible"
      title="找回密码"
      width="420px"
      :close-on-click-modal="false"
    >
      <div class="forgot-password-content">
        <div class="forgot-icon">
          <el-icon :size="48" color="#667eea">
            <Lock />
          </el-icon>
        </div>
        <h3 class="forgot-title">重置您的密码</h3>
        <p class="forgot-description">
          请输入您的邮箱地址，我们将向您发送密码重置链接
        </p>

        <el-form
          ref="forgotFormRef"
          :model="forgotForm"
          :rules="forgotRules"
        >
          <el-form-item prop="email">
            <el-input
              v-model="forgotForm.email"
              placeholder="请输入注册邮箱"
              prefix-icon="Message"
              clearable
              class="modern-input"
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="forgotPasswordVisible = false" class="cancel-btn">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="resetLoading"
            @click="handleResetPassword"
            class="reset-btn"
          >
            发送重置链接
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { Platform, Check, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loginFormRef = ref()
const forgotFormRef = ref()
const loading = ref(false)
const resetLoading = ref(false)
const forgotPasswordVisible = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
  login_type: 'password'
})

const forgotForm = reactive({
  email: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名或手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const forgotRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    loading.value = true

    await authStore.login(loginForm)
    ElMessage.success('登录成功，正在跳转...')

    // 延迟跳转，让用户看到成功消息
    setTimeout(() => {
      const redirect = route.query.redirect || getDefaultRoute()
      router.push(redirect)
    }, 1000)
  } catch (error) {
    console.error('Login error:', error)

    // 根据错误类型提供更友好的提示
    let errorMessage = '登录失败，请重试'
    if (error.message) {
      if (error.message.includes('用户名') || error.message.includes('密码')) {
        errorMessage = '用户名或密码错误'
      } else if (error.message.includes('网络')) {
        errorMessage = '网络连接失败，请检查网络'
      } else if (error.message.includes('服务器')) {
        errorMessage = '服务器暂时无法访问，请稍后重试'
      } else {
        errorMessage = error.message
      }
    }

    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 获取默认跳转路由
const getDefaultRoute = () => {
  // 登录后统一跳转到管理后台
  return '/admin'
}

// 显示忘记密码对话框
const showForgotPassword = () => {
  forgotPasswordVisible.value = true
}

// 发送重置密码邮件
const handleResetPassword = async () => {
  try {
    await forgotFormRef.value.validate()
    resetLoading.value = true

    await authAPI.sendResetPasswordEmail({
      email: forgotForm.email
    })

    ElMessage.success('重置链接已发送到您的邮箱，请查收')
    forgotPasswordVisible.value = false

    // 清空表单
    Object.assign(forgotForm, {
      email: ''
    })
  } catch (error) {
    ElMessage.error(error.message || '发送失败，请检查邮箱地址是否正确')
  } finally {
    resetLoading.value = false
  }
}

onMounted(() => {
  // 设置页面标题
  document.title = '用户登录 - 防腐保温行业平台'

  // 如果已经登录，直接跳转
  if (authStore.isLoggedIn) {
    router.push(getDefaultRoute())
  }

  // 添加全局错误处理
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)
    ElMessage.error('系统出现异常，请刷新页面重试')
  })
})
</script>

<style scoped>
/* 当使用AuthLayout时，移除背景样式 */





@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表单区域 - 简洁白色风格 */
.form-section {
  width: 100%;
  padding: 0;
}

.form-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

@keyframes formSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 55px;
  height: 55px;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border-radius: 14px;
  margin-bottom: 12px;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.platform-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 6px;
}

.form-subtitle {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.login-form {
  margin-bottom: 30px;
}

.input-wrapper {
  position: relative;
  margin-bottom: 4px;
}

.modern-input {
  transition: all 0.3s ease;
}

.modern-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  box-shadow: none;
  transition: all 0.3s ease;
  background: #f9fafb;
}

.modern-input :deep(.el-input__wrapper:hover) {
  border-color: #3b82f6;
  background: #ffffff;
}

.modern-input :deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: #ffffff;
}

.modern-input :deep(.el-input__inner) {
  font-size: 15px;
  color: #374151;
  height: 48px;
}

.modern-input :deep(.el-input__prefix) {
  color: #9ca3af;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-checkbox :deep(.el-checkbox__label) {
  color: #6b7280;
  font-size: 14px;
}

.forgot-link {
  font-size: 14px;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #1d4ed8;
}

.login-button {
  width: 100%;
  height: 46px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.login-button:disabled:hover {
  transform: none;
  box-shadow: none;
}

.form-footer {
  text-align: center;
  margin-top: 30px;
}

.register-prompt {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.register-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

/* 忘记密码对话框样式 */
.forgot-password-content {
  text-align: center;
  padding: 20px 0;
}

.forgot-icon {
  margin-bottom: 20px;
}

.forgot-title {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.forgot-description {
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 30px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 8px 20px;
  border-radius: 8px;
}

.reset-btn {
  padding: 8px 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  border: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-section {
    padding: 20px 15px;
  }

  .form-container {
    max-width: 100%;
    padding: 40px 30px;
    border-radius: 20px;
  }

  .platform-title {
    font-size: 18px;
  }

  .form-title {
    font-size: 24px;
  }

  .logo-icon {
    width: 50px;
    height: 50px;
  }
}

@media (max-width: 480px) {
  .form-section {
    padding: 15px 10px;
  }

  .form-container {
    padding: 30px 25px;
    border-radius: 16px;
  }

  .platform-title {
    font-size: 16px;
  }

  .form-title {
    font-size: 22px;
  }

  .logo-icon {
    width: 45px;
    height: 45px;
  }
}
</style>
